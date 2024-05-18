import sys, os
from config import SRC
srcdir = SRC
testdir = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

from agent_service.tools import web_search_tool
import unittest

sys.path.insert(0, os.path.abspath(testdir))
class TestWebSearchTool(unittest.TestCase):
    res_dict = { "organic_results":[
            {
            "position": 1,
            "title": "Coffee",
            "link": "https://en.wikipedia.org/wiki/Coffee",
            "redirect_link": "https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://en.wikipedia.org/wiki/Coffee&ved=2ahUKEwiR5vqbm5KDAxUJSzABHetUBPsQFnoECA8QAQ",
            "displayed_link": "https://en.wikipedia.org › wiki › Coffee",
            "thumbnail": "https://serpapi.com/searches/644b696a15afff2c2fdb8474/images/ed8bda76b255c4dc4634911fb134de5319e08af7e374d3ea998b50f738d9f3d2.jpeg",
            "favicon":  "https://serpapi.com/searches/647d7f362c2c2a3962879557/images/eaae281147a6573e1938c032f47c3595217b0dd06301405bb682756bcef85f10.png",
            "snippet": "Coffee is a beverage prepared from roasted coffee beans. Darkly colored, bitter, and slightly acidic, coffee has a stimulating effect on humans, ...",
            "snippet_highlighted_words": [
                "Coffee",
                "coffee",
                "coffee"
            ],
            },
            {
            "position": 2,
            "title": "The Coffee Bean & Tea Leaf | CBTL",
            "link": "https://www.coffeebean.com/",
            "redirect_link": "https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://www.coffeebean.com/&ved=2ahUKEwj3gdzSm5KDAxXdIEQIHW5OCPkQFnoECAkQAQ",
            "displayed_link": "https://www.coffeebean.com",
            "favicon":  "https://serpapi.com/searches/647d7f362c2c2a3962879557/images/eaae281147a6573e1938c032f47c3595277a9cb2cabd3d308557d74427b8c62d.png",
            "snippet": "Born and brewed in Southern California since 1963, The Coffee Bean & Tea Leaf® is passionate about connecting loyal customers with carefully handcrafted ...",
            "snippet_highlighted_words": [
                "Coffee"
            ],
        }
    ]
}
    
    def test_parse_contains(self):
        """
        The function `test_simple_substitute` tests the parsing of search results for specific text patterns
        using regular expressions.
        """
        tool = web_search_tool.WebSearch()
        res = tool.parse_results(self.res_dict)
        self.assertRegexpMatches(res, r"Coffee is a beverage prepared from roasted coffee beans.")
        self.assertRegexpMatches(res, r"Born and brewed in Southern California since 1963, The Coffee Bean & Tea Leaf® is passionate about connecting loyal")

    def test_parse_not_contain(self):
        """
        The function `test_simple_substitute` tests the parsing of search results for specific text patterns
        using regular expressions.
        """
        tool = web_search_tool.WebSearch()
        res = tool.parse_results(self.res_dict)
        self.assertNotRegexpMatches(res, r"https://www.coffeebean.com/")
        self.assertNotRegexpMatches(res, r"https://en.wikipedia.org › wiki › Coffee")


if __name__ == '__main__':
    unittest.main()