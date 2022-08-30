from datetime import datetime

def sample_responses (input_text):
    user_msg = str(input_text).lower()

    if user_msg in ("hi", "yo"):
        return "Wassap bro"

    if user_msg in ("what r u", "what are you?"):
        return "you made me how tf you forget"

    if user_msg in ("what time is it"):
        time_now = datetime.now()
        date_time = time_now.strftime("%d/%m/%y")

        return str(date_time)

    return "idgi can you say again"