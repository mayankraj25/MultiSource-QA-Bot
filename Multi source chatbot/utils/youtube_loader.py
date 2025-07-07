from langchain_community.document_loaders import YoutubeLoader

def load_youtube(video_url):
    loader = YoutubeLoader.from_youtube_url(video_url)
    return loader.load()
