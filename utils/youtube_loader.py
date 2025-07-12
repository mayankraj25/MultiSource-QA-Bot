from langchain_community.document_loaders import YoutubeLoader
from youtube_transcript_api import YouTubeTranscriptApi

def load_youtube(video_url):
    loader = YoutubeLoader.from_youtube_url(video_url)
    return loader.load()
