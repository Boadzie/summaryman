from io import BytesIO
import base64
from fastapi import FastAPI
from starlette.requests import Request
from fastapi.templating import Jinja2Templates
import nltk
from nltk.tokenize import sent_tokenize
from gensim.summarization import summarize
from wordcloud import WordCloud, STOPWORDS 

app = FastAPI()

templates = Jinja2Templates(directory="templates")


nltk.download('punkt') # download this
@app.get("/")
def home(request: Request):
    
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/")
async def home(request: Request):
    sumary=""
    if request.method == "POST": 
        form = await request.form()
        if form["message"] and form["word_count"]: 
            word_count = form["word_count"]
            text = form["message"]
            sumary = summarize(text, word_count=int(word_count))
            sentences = sent_tokenize(sumary) # tokenize it
            sents = set(sentences)
            sumary = ' '.join(sents) 
            word_cloud = wordcloud(sumary)
            # img = BytesIO(word_cloud)
            # img.seek(0)
            # file_bytes = np.asarray(bytearray(img.read()), dtype=np.uint8)
            # frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    return templates.TemplateResponse("index.html", {"request": request, "sumary": sumary, "wordcloud": word_cloud})



def wordcloud(text):
    stopwords = set(STOPWORDS)
    wordcloud = WordCloud(width = 800, height = 800, 
                background_color ='white', 
                stopwords = stopwords, 
                min_font_size = 10).generate(text).to_image()
    img = BytesIO()
    wordcloud.save(img, "PNG")
    img.seek(0)
    img_b64 = base64.b64encode(img.getvalue()).decode()
    return img_b64

    