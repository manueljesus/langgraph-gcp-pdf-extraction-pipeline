from src.tasks import get_file_from_bucket
from src.graph import PipelineState
from src.utils.hash import generate_file_hash

class GetFile:
    def __init__(
        self,
        file_name: str
    ):
        self.file_name = file_name

    def __call__(self, _: PipelineState):
        file = get_file_from_bucket(self.file_name)
        paper_id = generate_file_hash(file)

        return {
            "state": {
                "file": file,
                "paper_id": paper_id
            }
        }