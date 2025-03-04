import difflib

def check_content_length(original_length, response_length, threshold=50):
    #Kiểm tra xem độ dài của phản hồi
    difference = abs(response_length - original_length)
    
    if difference > threshold:
        return True
    else:
        return False 

def check_html_similarity(original_content, response_content, similarity_threshold=0.9):
    #So sánh mức độ giống nhau giữa phản hồi gốc và phản hồi sau khi chèn payload.
    similarity = difflib.SequenceMatcher(None, original_content, response_content).ratio()

    if similarity < similarity_threshold:
        return True 
    else:
        return False