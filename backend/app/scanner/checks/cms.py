from bs4 import BeautifulSoup
import re


class CMSDetector:
    """
    Performs passive technology and CMS detection.
    """


    CMS_SIGNATURES = {

        "WordPress": [
            "wordpress",
            "wp-content",
            "wp-includes",
            "wp-json",
        ],

        "Drupal": [
            "drupal",
            "/sites/default/",
        ],

        "Joomla": [
            "joomla",
            "/media/system/",
        ],

    }



    def analyze(self, context: dict) -> dict:
        """
        Analyze response headers and HTML content.

        Passive detection only.
        """


        response = context["response"]


        technologies = []

        cms_results = []

        detected = set()



        headers = response.headers



        server = headers.get(
            "Server"
        )


        if server:

            technologies.append(
                {
                    "name": "Server",
                    "value": server,
                }
            )



        powered_by = headers.get(
            "X-Powered-By"
        )


        if powered_by:

            technologies.append(
                {
                    "name": "X-Powered-By",
                    "value": powered_by,
                }
            )



        html = response.text.lower()



        soup = BeautifulSoup(
            response.text,
            "html.parser",
        )



        #
        # Generator meta tag detection
        #

        generator = soup.find(
            "meta",
            attrs={
                "name": "generator"
            },
        )


        if generator and generator.get(
            "content"
        ):


            content = generator.get(
                "content"
            )


            cms_name, version = self.extract_version(
                content
            )


            cms_results.append(
                {
                    "name": cms_name,
                    "version": version,
                    "source": "meta generator",
                }
            )


            detected.add(
                cms_name
            )



        #
        # Signature based detection
        #

        for cms_name, signatures in self.CMS_SIGNATURES.items():


            if cms_name in detected:

                continue



            for signature in signatures:


                if signature in html:


                    cms_results.append(
                        {
                            "name": cms_name,
                            "version": None,
                            "source": "html signature",
                        }
                    )


                    detected.add(
                        cms_name
                    )


                    break



        return {

            "technologies": technologies,

            "cms": cms_results,

        }




    def extract_version(
        self,
        value: str
    ):
        """
        Extract CMS name and version
        from generator strings.

        Example:
        WordPress 6.5.2
        """


        patterns = {

            "WordPress": r"wordpress\s*([0-9.]+)?",

            "Drupal": r"drupal\s*([0-9.]+)?",

            "Joomla": r"joomla!?\s*([0-9.]+)?",

        }



        lower_value = value.lower()



        for name, pattern in patterns.items():


            match = re.search(
                pattern,
                lower_value,
            )


            if match:


                return (

                    name,

                    match.group(1)

                )



        return (

            value,

            None

        )