import dspy

class DSPyExtractor:
    """Class for extracting structured information from text using DSPy."""

    def __init__(self, model: str, api_base: str, api_key: str):
        import dspy
        self.lm = dspy.LM(
            f'ollama_chat/{model}',
            api_base=api_base,
            api_key=api_key,
            model_type="chat"
        )
        dspy.configure(lm=self.lm)

    async def extract_info(self, text: str) -> dict:
        """Extract structured information from the given text."""
        extractor = dspy.Predict(ExtractInfo)
        result = await extractor.acall(text=text)
        return {
            "title": result.title,
            "headings": result.headings,
            "entities": result.entities
        }

class ExtractInfo(dspy.Signature):
    """Extract structured information from text."""
    text: str = dspy.InputField()
    title: str = dspy.OutputField()
    headings: list[str] = dspy.OutputField()
    entities: list[dict[str, str]] = dspy.OutputField(desc="a list of entities and their metadata")
