import re

from bs4 import BeautifulSoup



class CMSDetector:
    """
    Performs passive technology and CMS detection.
    """


    CMS_SIGNATURES = {

        "WordPress": [

            "wordpress",
            "wp-content",
            "wp-includes",

        ],

        "Drupal": [

            "drupal",

        ],

        "Joomla": [

            "joomla",

        ],

    }




    VERSION_PATTERNS = {

        "WordPress": [

            r"wp[-_/].*?ver=([0-9]+\.[0-9]+(?:\.[0-9]+)?)",

            r"wordpress\s*([0-9]+\.[0-9]+(?:\.[0-9]+)?)",

        ],

        "Drupal": [

            r"drupal[-\s]?([0-9]+)",

        ],

        "Joomla": [

            r"joomla[-\s]?([0-9]+(?:\.[0-9]+)?)",

        ],

    }




    def analyze(
        self,
        context: dict
    ) -> dict:
        """
        Analyze response headers and HTML content.
        """


        response = context["response"]


        technologies = []

        cms = []


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

            "html.parser"

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



        if generator and generator.get("content"):


            content = generator.get(
                "content"
            )


            detected = self._parse_generator(
                content
            )


            cms.append(
                detected
            )




        #
        # Signature based detection
        #

        for cms_name, signatures in self.CMS_SIGNATURES.items():


            detected = False


            for signature in signatures:


                if signature in html:

                    detected = True

                    break



            if detected and not self._already_detected(
                cms,
                cms_name
            ):


                version = self._detect_version(

                    cms_name,

                    response.text

                )



                cms.append(

                    {

                        "name": cms_name,

                        "version": version,

                        "source": "html signature",

                    }

                )





        return {

            "technologies": technologies,

            "cms": cms,

        }





    def _parse_generator(
        self,
        value: str
    ) -> dict:
        """
        Parse CMS information from generator tag.
        """


        value_lower = value.lower()



        for cms_name in self.CMS_SIGNATURES:


            if cms_name.lower() in value_lower:


                version = self._extract_version(
                    value
                )


                return {

                    "name": cms_name,

                    "version": version,

                    "source": "meta generator",

                }



        return {

            "name": value,

            "version": None,

            "source": "meta generator",

        }




    def _detect_version(
        self,
        cms_name: str,
        content: str
    ):
        """
        Detect passive CMS version hints.
        """


        patterns = self.VERSION_PATTERNS.get(

            cms_name,

            []

        )



        for pattern in patterns:


            match = re.search(

                pattern,

                content,

                re.IGNORECASE

            )


            if match:

                return match.group(1)




        return None





    def _extract_version(
        self,
        value: str
    ):


        match = re.search(

            r"([0-9]+\.[0-9]+(?:\.[0-9]+)?)",

            value

        )


        if match:

            return match.group(1)



        return None





    def _already_detected(
        self,
        cms,
        name
    ) -> bool:


        for item in cms:


            if item.get("name") == name:

                return True



        return False