import os
import pytest
import yaml
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
driver = None
# ---------- Helper to read URLs from YAML ----------
#def load_config():
    #config_path = os.path.join(os.path.dirname(__file__), "config.yaml")
    #with open(config_path,"r") as f:
        #return yaml.safe_load(f)

# ---------- Add custom CLI options ----------
def pytest_addoption(parser):
    parser.addoption("--browser_name", action="store", default="Edge", help="browser selection")
    parser.addoption("--url_key", action="store", default="SwagLabs", help="Choose URL key")
    parser.addoption("--headless", action="store_true", help="Run browser in headless mode")

URL_MAP = {"SwagLabs": "https://www.saucedemo.com/v1/index.html"}

@pytest.fixture(scope="function")
def browserInstance(request):
    global driver

    browser_name = request.config.getoption("browser_name")
    url_key = request.config.getoption("url_key")
    headless = request.config.getoption("headless")

    #config = load_config()
    #base_url = config["urls"].get(url_key)
    #if not base_url:
        #raise ValueError(f"URL key '{url_key}' not found in config.yaml")
    base_url = URL_MAP.get(url_key)

    #--- Browser setup ---
    if browser_name == "chrome":
        chrome_options = ChromeOptions()
        if headless:
            chrome_options.add_argument("headless")
        driver = webdriver.Chrome(options=chrome_options)
    elif browser_name == "firefox":
        firefox_options = FirefoxOptions()
        if headless:
            firefox_options.add_argument("headless")
        driver = webdriver.Firefox(options=firefox_options)
    elif browser_name == "IE":
        driver = webdriver.Ie()
    elif browser_name == "Edge":
        edge_options = EdgeOptions()
        if headless:
            edge_options.add_argument("headless")
        driver = webdriver.Edge(options=edge_options)
    driver.maximize_window()
    driver.implicitly_wait(3)
    driver.get(base_url)
    yield driver
    driver.quit()


@pytest.hookimpl( hookwrapper=True )
def pytest_runtest_makereport(item):
    """
        Extends the PyTest Plugin to take and embed screenshot in html report, whenever test fails.
        :param item:
        """
    pytest_html = item.config.pluginmanager.getplugin( 'html' )
    outcome = yield
    report = outcome.get_result()
    extra = getattr( report, 'extra', [] )

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr( report, 'wasxfail' )
        if (report.skipped and xfail) or (report.failed and not xfail):
            reports_dir = os.path.join( os.path.dirname( __file__ ), 'reports' )
            file_name = os.path.join( reports_dir, report.nodeid.replace( "::", "_" ) + ".png" )
            print( "file name is " + file_name )
            _capture_screenshot( file_name )
            if file_name:
                html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % file_name
                extra.append( pytest_html.extras.html( html ) )
        report.extras = extra

def _capture_screenshot(file_name):
    driver.get_screenshot_as_file(file_name)
