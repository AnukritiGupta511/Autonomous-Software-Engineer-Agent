import os
import uuid
from typing import List, Dict, Any

class CodeChunker:
    """A naive code chunker for RAG processing."""
    
    @staticmethod
    def chunk_file(file_path: str, content: str, chunk_size: int = 500, overlap: int = 50) -> List[Dict[str, Any]]:
        """Splits file content into overlapping chunks based on lines."""
        ext = os.path.splitext(file_path)[1].lower()
        language = CodeChunker.detect_language(ext)
        
        lines = content.splitlines()
        chunks = []
        
        current_chunk = []
        current_length = 0
        start_line = 1
        
        for i, line in enumerate(lines):
            # Very rough token approximation (words/pieces)
            line_len = len(line.split()) + 1 
            
            if current_length + line_len > chunk_size and current_chunk:
                chunk_text = "\n".join(current_chunk)
                chunks.append({
                    "id": f"{file_path}_{start_line}_{i}",
                    "content": chunk_text,
                    "metadata": {
                        "file_path": file_path,
                        "language": language,
                        "start_line": start_line,
                        "end_line": i
                    }
                })
                
                # Create overlap by keeping last N lines roughly equal to overlap tokens
                overlap_lines = []
                overlap_len = 0
                for r_line in reversed(current_chunk):
                    if overlap_len >= overlap:
                        break
                    overlap_lines.insert(0, r_line)
                    overlap_len += len(r_line.split()) + 1
                    
                current_chunk = overlap_lines
                current_length = overlap_len
                start_line = i - len(overlap_lines) + 1
                
            current_chunk.append(line)
            current_length += line_len
            
        # Add final chunk
        if current_chunk:
            chunks.append({
                "id": f"{file_path}_{start_line}_{len(lines)}",
                "content": "\n".join(current_chunk),
                "metadata": {
                    "file_path": file_path,
                    "language": language,
                    "start_line": start_line,
                    "end_line": len(lines)
                }
            })
            
        return chunks

    @staticmethod
    def detect_language(ext: str) -> str:
        mapping = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.jsx': 'react',
            '.tsx': 'react-ts',
            '.java': 'java',
            '.md': 'markdown',
            '.json': 'json',
            '.html': 'html',
            '.css': 'css',
            '.rs': 'rust',
            '.go': 'go'
        }
        return mapping.get(ext, 'unknown')
