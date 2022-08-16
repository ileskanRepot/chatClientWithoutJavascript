#!/usr/bin/env python
import socket

class WrongAmountExpection(Exception):
  """Raise for my specific kind of exception"""

class NotMsgOrSenderExpection(Exception):
  """Raise for my specific kind of exception"""

def parseHeader(headerString):
  headerList = headerString.split("\n")
  firstLineList = headerList[0].split(" ")
  headerDic = {
    "REQUEST": {
      "TYPE": firstLineList[0],
      "PATH": firstLineList[1],
      "PROTOCOL": firstLineList[2]
      
    }
  }
  return headerDic

def renderChats(filename):
  if ".." in filename or "~" in filename:
    print ("Error you fool")
    return "Don't even try"
  chatList = open("pages/"+filename, "r").read().split("\n")
  chatString = "<div class=\"SenderMsg\"><p class=\"Sender\">Sender</p><p class=\"Msg\">Msg</p></div>\n"
  for chat in chatList:
    if chat:
      chatChanged = chat.replace("<", "&lt;").replace(">", "&gt;")
      chatSplit = chatChanged.split(",")
      chatString += "<div class=\"SenderMsg\"><p class=\"Sender\">" + chatSplit[0] + "</p><p class=\"Msg\">" + chatSplit[1] + "</p></div>\n"
  return chatString

def parsePostRequest(request,filename):
  msg, sender = "", ""
  wholeMsg = request.split("\r\n\r\n")[1]
  splittedMsg = wholeMsg.split("&")
  if len(splittedMsg) != 2:
    raise WrongAmountExpection
  firstPart = splittedMsg[0].split("=")
  if firstPart[0] == "sender":
    sender = firstPart[1].replace("+", " ")
  elif firstPart[0] == "msg":
    msg = firstPart[1].replace("+", " ")
  else:
    raise NotMsgOrSenderExpection(firstPart[0])

  secondPart = splittedMsg[1].split("=")
  if secondPart[0] == "sender":
    sender = secondPart[1].replace("+", " ")
  elif secondPart[0] == "msg":
    msg = secondPart[1].replace("+", " ")
  else:
    raise NotMsgOrSenderExpection(secondPart[0])

  if sender == "" or msg == "":
    raise NotMsgOrSenderExpection(". You missed other")

  chatFile = open("pages/"+filename, "a")
  chatFile.write("\n"+sender+","+msg)
  return "<p>SUCCESS</p>"

def main():
  # Define socket host and port
  SERVER_HOST = '0.0.0.0'
  SERVER_PORT = 8000
  
  # Create socket
  server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  server_socket.bind((SERVER_HOST, SERVER_PORT))
  server_socket.listen(1)

  print('Listening on port %s ...' % SERVER_PORT)
  
  while True:
    # Wait for client connections
    client_connection, client_address = server_socket.accept()
  
    print("Requested")
    # Get the client request
    requestRaw = client_connection.recv(1024)
    request = requestRaw.decode()

    headers = parseHeader(request)
    
    upperHtml = open("upperHalf.html", "r").read()
    bottomHtml = open("bottomHalf.html", "r").read()
    # chatFile = for i in requset.split("\n") if i 
  
    # print("Header Type:",headers["REQUEST"]["TYPE"])
    # print("Header Path:",headers["REQUEST"]["PATH"])
    # print("Header Protocol:",headers["REQUEST"]["PROTOCOL"])
    # parsePostRequest(request)
    try:
      response = "HTTP/1.0 200 OK\n\n"
      chatFile = headers["REQUEST"]["PATH"].split("/")[1].replace("?","")
      if chatFile == "favicon.ico":
        response += "You idiot tried to get my favicon"
      elif headers["REQUEST"]["TYPE"] == "POST":
        tmpResponce = parsePostRequest(request,chatFile)
        response += upperHtml
        response += renderChats(chatFile)
        response += tmpResponce
        response += bottomHtml
      else:
        response += upperHtml
        response += renderChats(headers["REQUEST"]["PATH"].replace("?",""))
        response += bottomHtml
    except FileNotFoundError:
      response = "HTTP/1.0 400 YOU STUPID\n\nFile \"" + headers["REQUEST"]["PATH"].replace("?","") + "\" Not found"
    except WrongAmountExpection as e:
      response = "HTTP/1.0 400 YOU STUPID\n\nWrong Amount"
    except NotMsgOrSenderExpection as e:
      response = "HTTP/1.0 400 YOU STUPID\n\nNot valid "+str(e)
    except:
      response = "HTTP/1.0 500 ME STUPID\n\nME STUPID"
    client_connection.sendall(response.encode())
    client_connection.close()

  # Close socket
  server_socket.close()


if __name__ == "__main__":
  main()
