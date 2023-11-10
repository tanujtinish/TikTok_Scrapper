import requests

#https://github.com/dbpedia-spotlight/dbpedia-spotlight-model
# https://arxiv.org/pdf/2005.13798.pdf

class EntityLinkingService:
    def __init__(self, api_url="https://api.dbpedia-spotlight.org/en/annotate", confidence=0.35):
        self.api_url = api_url
        self.confidence = confidence

    def link_entities(self, text):
        """
        Perform entity linking on the given text.

        Args:
            text (str): The text to annotate and link entities.

        Returns:
            list: A list of annotated entities with information such as URI, support, and surface form.
        """
        data = {
            "text": text,
            "confidence": self.confidence
        }

        headers = {
            "Accept": "application/json"
        }

        response = requests.post(self.api_url, data=data, headers=headers)

        if response.status_code == 200:
            entities = response.json()
            if "Resources" in entities:
                return [entity["@surfaceForm"] for entity in entities["Resources"]]
            else:
                return []
        else:
            return []

# Example usage
if __name__ == "__main__":
    # Create an instance of the EntityLinkingService
    entity_linking_service = EntityLinkingService()

    # Define the text to perform entity linking on
    text = "new feature alert 🚨more duet layouts available try two always better one show u perfect duet duet videolarını bir üst seviyeye taşımanın zamanı geldi i̇şte yaratıcılığına ilham verebilecek bazı ipuçları mükemmeliçerik"

    # Perform entity linking
    linked_entities = entity_linking_service.link_entities(text)

    # Print the linked entities
    for entity in linked_entities:
        print(entity)

