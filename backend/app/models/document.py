from datetime import datetime
from dataclasses import dataclass

@dataclass
class Document:
    id: str
    filename: str
    file_type: str
    file_size: int
    chunk_count: int
    status: str
    upload_date: datetime
    
    def to_dict(self):
        return {
            "id": self.id,
            "filename": self.filename,
            "file_type": self.file_type,
            "file_size": self.file_size,
            "chunk_count": self.chunk_count,
            "status": self.status,
            "upload_date": self.upload_date.isoformat()
        }