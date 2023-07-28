import sys
import requests
import smtplib
import email.message


def main():
    # checking for correct inputs.
    try:
        receiver = sys.argv[1]
        selected_api = sys.argv[2]
        api_key = sys.argv[3]
    except IndexError:
        print("Not enough arguments!")
        sys.exit()
    if "@" and "." not in receiver:
        print("Incorrect email format!")
        sys.exit()
    else:
        sender = input("Enter sender email: ")
        sender_password = input("Enter password: ")
        if "newsapi" in selected_api:
            message = news_api(api_key)
            email_sender(receiver, message, sender, sender_password)
            print("News sent.")
        elif "alphavantage" in selected_api:
            message = stock_api(api_key)
            email_sender(receiver, message, sender, sender_password)
            print("Stock sent.")
        else:
            print("Incorrect information provided!")
    # if info is correct, the program will go through either the first or the second elif statement,
    # it will return the message obtained from the api and pass it to the email_sender


def news_api(api_key):
    response = requests.get(
        f"https://newsapi.org/v2/top-headlines?country=lt&pageSize=1&apiKey={api_key}"
    )
    try:
        article = (
            "The top article in Lithuania today is:",
            response.json()["articles"][0]["url"],
        )
    except KeyError:
        print("Incorrect API key provided.")
        sys.exit()
    message = " ".join(article)

    return message


def stock_api(api_key):
    response = requests.get(
        f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=STN&apikey={api_key}"
    )
    try:
        stock_name = response.json()["Meta Data"]["2. Symbol"]
        stock_date = response.json()["Meta Data"]["3. Last Refreshed"]
        stock_price = response.json()["Time Series (Daily)"][str(stock_date)]["1. open"]
    except KeyError:
        print("Incorrect API key provided.")
        sys.exit()

    info = stock_name, "price for", stock_date + ": $" + stock_price
    message = " ".join(info)


    return message


def email_sender(receiver, message, sender, sender_password):
    m = email.message.Message()
    m["From"] = sender
    m["To"] = receiver
    m["Subject"] = "Test assignment!"
    m.set_payload(message)

    try:
        smtpObj = smtplib.SMTP("smtp.gmail.com", 587)
        smtpObj.starttls()
        smtpObj.login(sender, sender_password)
        smtpObj.sendmail(sender, receiver, m.as_string())
    except smtplib.SMTPAuthenticationError:
        print("Incorrect username or password!")
        sys.exit()


if __name__ == "__main__":
    main()
