from rich.console import Console
from rich.markdown import Markdown

from config import chat_log_file_name
from apis.youtube_client import get_video_comments, check_video_exists
from apis.openai_client import analyze_comments_in_batches
from chat.file import save_chat_to_file, clear_file, read_from_file

def main():
    stop_word = "quit"
    ulr_word = "url"
    
    clear_file(chat_log_file_name)
    
    print(f"\033[34m {stop_word.capitalize()} to exit, change video {ulr_word} \033[0m")
    video_url = input("\033[31m Enter YouTube video URL: \033[0m")
    
    
    console = Console()
    while True:
        if video_url.lower() == stop_word:
            break
        video_id = check_video_exists(video_url)
        if not video_id:
            video_url = input("\033[31m Enter YouTube video URL: \033[0m")
            continue
        
        user_query = input("\033[90m User: \033[0m")
        if user_query.lower() == stop_word:
            break  
        elif user_query.lower() == ulr_word:
            video_url = input("\033[31m Enter YouTube video URL: \033[0m")
            clear_file(chat_log_file_name)
            continue
        
        chat_history = read_from_file(chat_log_file_name)
        comments = get_video_comments(video_id)
        
        gpt_query = analyze_comments_in_batches(comments, user_query, chat_history)
        
        save_chat_to_file(chat_log_file_name, user_query, "User: ")
        save_chat_to_file(chat_log_file_name, gpt_query, "GPT: ")
        
        gpt_query_to_console = Markdown(gpt_query)
        console.print("[cyan] ChatGPT: [/cyan]", end="")
        console.print(gpt_query_to_console, end="\n")
        
    clear_file(chat_log_file_name)

if __name__ == "__main__":
    main()