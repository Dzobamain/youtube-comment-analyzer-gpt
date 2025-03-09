from rich.console import Console
from rich.markdown import Markdown

from config import chat_log_file_name

from apis.youtube_client import get_video_comments, check_video_exists
from apis.openai_client import analyze_comments_in_batches
from chat.file import save_chat_to_file, clear_file, read_from_file

def url_input(video_url, stop_word):
    while True:
        if video_url.lower() == stop_word:
            return False
        video_id = check_video_exists(video_url)
        if not video_id:
            video_url = input("\033[31m Enter YouTube video URL: \033[0m")
            continue
        else:
            return video_id

def main():
    isStart = True
    stop_word = "quit"
    ulr_word = "url"
    console = Console()
    chat_history = ""
    clear_file(chat_log_file_name)
    
    print(f"\033[34m {stop_word.capitalize()} to exit, change video {ulr_word} \033[0m")
    
    video_url = input("\033[31m Enter YouTube video URL: \033[0m")
    video_id = url_input(video_url, stop_word)
    if not video_id:
        return
    comments = get_video_comments(video_id)
    
    while isStart:
        user_query = input("\033[90m User: \033[0m")
        if user_query.lower() == stop_word:
            break  
        elif user_query.lower() == ulr_word:
            video_url = input("\033[31m Enter YouTube video URL: \033[0m")
            video_id = url_input(video_url, stop_word)
            
            if not video_id:
                isStart = False
            comments = get_video_comments(video_id)
            clear_file(chat_log_file_name)
        
        gpt_query = analyze_comments_in_batches(comments, user_query, chat_history)
        
        save_chat_to_file(chat_log_file_name, user_query + "\n\n", "User: ")
        save_chat_to_file(chat_log_file_name, gpt_query + "\n\n", "GPT: ")
        
        gpt_query_to_console = Markdown(gpt_query)
        console.print("[cyan] ChatGPT: [/cyan]", end="")
        console.print(gpt_query_to_console, end="\n")
        
        chat_history = read_from_file(chat_log_file_name)
        
    clear_file(chat_log_file_name)
    
if __name__ == "__main__":
    main()