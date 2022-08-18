#!/usr/bin/env python
import socket
import sys
import os

class WrongAmountExpection(Exception):
  """Raise for my specific kind of exception"""

class NotMsgOrSenderExpection(Exception):
  """Raise for my specific kind of exception"""

class NoProtocolExpection(Exception):
  """Raise for my specific kind of exception"""

class FileNameTooLongExpection(Exception):
  """Raise for my specific kind of exception"""

class IllegalFilenameExpection(Exception):
  """Raise for my specific kind of exception"""

def parseHeader(headerString):
  headerList = headerString.split("\n")
  firstLineList = headerList[0].split(" ")
  if len(firstLineList) < 3:
    raise NoProtocolExpection
  headerDic = {
    "REQUEST": {
      "TYPE": firstLineList[0],
      "PATH": firstLineList[1],
      "PROTOCOL": firstLineList[2]
      
    }
  }
  return headerDic

def illegalFilenameCheck(filename):
  if ".." in filename or "~" in filename:
    return False
  

def renderChats(filename):
  if illegalFilenameCheck(filename):
    print ("Error you fool")
    raise IllegalFilenameExpection
  chatList = open("pages/"+filename, "r").read().split("\n")
  chatString = "<div class=\"SenderMsg\"><p class=\"Sender\">Sender</p><p class=\"Msg\">Msg</p></div>\n"
  for chat in chatList:
    if chat:
      chatChanged = chat.replace("<", "&lt;").replace(">", "&gt;")
      chatSplit = chatChanged.split(",")
      if len(chatSplit) != 2:
        continue
      chatString += "<div class=\"SenderMsg\"><p class=\"Sender\">" + chatSplit[0] + "</p><p class=\"Msg\">" + chatSplit[1] + "</p></div>\n"
  return chatString

def parsePostRequest(request,filename):
  msg, sender = "", ""
  requestSplit = request.split("\r\n\r\n")
  if len(requestSplit) != 2:
    print("RequestSplit")
    raise WrongAmountExpection
  wholeMsg = requestSplit[1]
  splittedMsg = wholeMsg.split("&")
  if len(filename) > 255:
    raise FileNameTooLongExpection(filename)
  if len(splittedMsg) != 2:
    raise WrongAmountExpection
  if ".." in filename or "~" in filename:
    print ("Error you fool")
    raise IllegalFilenameExpection

  firstPart = splittedMsg[0].split("=")
  if len(firstPart) != 2:
    raise WrongAmountExpection
  if firstPart[0] == "sender":
    sender = firstPart[1].replace("+", " ").replace("\n", "")
  elif firstPart[0] == "msg":
    msg = firstPart[1].replace("+", " ").replace("\n", "")
  else:
    raise NotMsgOrSenderExpection(firstPart[0])

  secondPart = splittedMsg[1].split("=")
  if len(secondPart) != 2:
    raise WrongAmountExpection
  if secondPart[0] == "sender":
    sender = secondPart[1].replace("+", " ").replace("\n", "")
  elif secondPart[0] == "msg":
    msg = secondPart[1].replace("+", " ").replace("\n", "")
  else:
    raise NotMsgOrSenderExpection(secondPart[0])

  if illegalFilenameCheck(filename):
    raise NotMsgOrSenderExpection(". You missed other")

  chatFile = open("pages/"+filename, "a")
  chatFile.write("\n"+sender+","+msg)
  return "<p>SUCCESS</p>"

def renderChatRooms(path):
  chatRoomHtml = ""
  rooms = os.listdir(path)
  for room in rooms:
    chatRoomHtml += "<p><a href=/" + room + ">" + room + "</a></p>"
  return chatRoomHtml

def printErr(msg):
  print(msg, file=sys.stderr)

def main():
  # Define socket host and port
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.connect(("8.8.8.8", 80))
  ip = s.getsockname()[0]
  s.close()
  print(ip)

  SERVER_HOST = 'localhost'
  SERVER_ADDR = (ip, 8000)
  SERVER_PORT = 8000
  
  # Create socket
  server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  server_socket.bind(SERVER_ADDR)
  server_socket.listen(1)

  print('Listening on port %s ...' % SERVER_PORT)
  
  while True:
    # Wait for client connections
    client_connection, client_address = server_socket.accept()
  
    print("Requested")
    # Get the client request
    requestRaw = client_connection.recv(1024)
    print("requestRaw:\n"+str(requestRaw))
    try:
      request = requestRaw.decode()
    except:
      continue

    upperHtml = open("upperHalf.html", "r").read()
    bottomHtml = open("bottomHalf.html", "r").read()
    # chatFile = for i in requset.split("\n") if i 
  
    # print("Header Type:",headers["REQUEST"]["TYPE"])
    # print("Header Path:",headers["REQUEST"]["PATH"])
    # print("Header Protocol:",headers["REQUEST"]["PROTOCOL"])
    # parsePostRequest(request)
    try:
      headers = parseHeader(request)
      response = ""
      chatFile = headers["REQUEST"]["PATH"].split("/")[1]
      print("chatFile",chatFile)
      print("headers",headers["REQUEST"]["PATH"])
      if chatFile == "favicon.ico":
        response += "HTTP/1.0 400 You rly\n\n"
        response += "You idiot tried to get my favicon"
      elif chatFile == "":
        response += "HTTP/1.0 200 OK\n\n"
        response += "<h1>Chat rooms:</h1>"
        response += renderChatRooms("pages")
        response += "<p>To add new chat room contact server hoster or just POST there without GETing</p>"
      elif headers["REQUEST"]["TYPE"] == "POST":
        if chatFile[-1] == "?":
          print("WEE WOO")
          chatFile = chatFile[:-1]
          response += "HTTP/1.0 301 Redirect\nLocation: " + chatFile + "\n\n"
        else:
          response += "HTTP/1.0 200 OK\n\n"
        tmpResponce = parsePostRequest(request,chatFile)
        response += upperHtml
        response += renderChats(chatFile)
        response += tmpResponce
        response += bottomHtml
      else:
        response += "HTTP/1.0 200 OK\n\n"
        response += upperHtml
        response += renderChats(chatFile.replace("?",""))
        response += bottomHtml
    except FileNotFoundError:
      print("")
      response = "HTTP/1.0 400 YOU STUPID\n\nFile \"" + headers["REQUEST"]["PATH"].replace("?","") + "\" Not found"
    except WrongAmountExpection as e:
      print("WRONG AMOUNT OF PARAMETERS")
      response = "HTTP/1.0 400 YOU STUPID\n\nWrong Amount"
    except NotMsgOrSenderExpection as e:
      print("NOT VALID POST PARAMETERS")
      response = "HTTP/1.0 400 YOU STUPID\n\nNot valid "+str(e)
    except NoProtocolExpection as e:
      print("NO PROTOCOL DEFINED")
      response = "HTTP/1.0 400 YOU STUPID\n\nNo all parameters"
    except FileNameTooLongExpection as e:
      print("CHAT NAME TOO LONG")
      response = "HTTP/2.0 400 YOU STUPID\n\nChat name too long " + str(e)
    except IllegalFilenameExpection as e:
      print("ILLEGAL CHAT NAME")
      response = "HTTP/2.0 400 YOU STUPID\n\nIllegal chat name " + str(e)
    except Exception as e:
      printErr("error "+str(e))
      response = "HTTP/1.0 500 ME STUPID\n\nME STUPID"
    client_connection.sendall(response.encode())
    client_connection.close()

  # Close socket
  server_socket.close()


if __name__ == "__main__":
  main()
