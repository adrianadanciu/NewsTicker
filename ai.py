import streamlit as st
import torch #librabry for machine learning
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline #import instruments for ai usage

@st.cache_resource(show_spinner=False) #gives the user the most recent seached news
def load_local_finbert(): #download the ai
    model_name = "ProsusAI/finbert"
    tokenizer = AutoTokenizer.from_pretrained(model_name, local_files_only=False)
    model = AutoModelForSequenceClassification.from_pretrained(model_name, local_files_only=False)
    return tokenizer, model

def analyze_headlines(headlines):
    tokenizer, model = load_local_finbert()
    """Processes headlines using FinBERT to deduce stock movements from technical news. Returns aggregated counts plus the original headlines enriched with per-item sentiment."""
    total_positive = 0
    total_negative = 0
    total_neutral = 0
    future_dilution = False
    future_growth = False
    enriched_headlines = []  
    for item in headlines:
        text_upper = item["text"].upper()
        source = item["source"]
        tech_positive_catalysts = [
            "BENCHMARK BEAT", "NEW CHIP", "REVOLUTIONARY", "UPDATE RELEASED", "PATCHED", 
            "OPEN SOURCE", "AI MODELS", "PERFORMANCE LEAP", "PARTNERSHIP", "BREAKTHROUGH"
        ] 
        tech_negative_catalysts = [
            "SECURITY FLAW", "VULNERABILITY", "EXPLOIT", "HACKED", "DELAY", "BUG", 
            "LEAKED", "LAWSUIT", "SUED", "ANTITRUST", "RECALL", "CRITICAL ERROR"
        ]
        dilution_catalysts = [
            "SECONDARY OFFERING", "SHARE DILUTION", "STOCK OFFERING", "INSIDER SELLING",
            "CONVERTIBLE NOTES", "EQUITY OFFERING", "SHELF OFFERING", "SHARE ISSUANCE"
        ]
        tech_sentiment_boost = None 
        if any(kw in text_upper for kw in tech_positive_catalysts):
            tech_sentiment_boost = "POSITIVE"
            future_growth = True
        elif any(kw in text_upper for kw in tech_negative_catalysts):
            tech_sentiment_boost = "NEGATIVE"
        if any(kw in text_upper for kw in dilution_catalysts):
            future_dilution = True
        inputs = tokenizer(item["text"], padding=True, truncation=True, return_tensors='pt') #prepares the data for the finbert model
        with torch.no_grad():
            outputs = model(**inputs)
        #decides the sentiment for the news (postive, negative, neutral)
        logits = outputs.logits[0]
        max_idx = torch.argmax(logits).item()
        #calculates the probability of the sentiment
        probs = torch.nn.functional.softmax(logits, dim=-1)
        confidence = probs[max_idx].item() * 100
        final_sentiment = None
        if tech_sentiment_boost:
            final_sentiment = tech_sentiment_boost
        else:
            if max_idx == 0:
                final_sentiment = "POSITIVE"
            elif max_idx == 1:
                final_sentiment = "NEGATIVE"
            else:
                final_sentiment = "NEUTRAL"
        if final_sentiment == "POSITIVE":
            total_positive += 1
        elif final_sentiment == "NEGATIVE":
            total_negative += 1
        else:
            total_neutral += 1
        enriched_headlines.append({
            **item,
            "sentiment": final_sentiment,
            "confidence": confidence,
        })
    #the news are ordered: the neutral ones are at the end
    enriched_headlines.sort(
        key=lambda h: (0 if h["sentiment"] != "NEUTRAL" else 1, -h["confidence"])
    )  
    return total_positive, total_negative, total_neutral, future_dilution, future_growth, enriched_headlines