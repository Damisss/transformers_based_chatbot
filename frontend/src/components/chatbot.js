import React, { useState, useEffect, useRef } from "react";
import {connect} from 'react-redux'
import {chatActionStart} from '../reducer/chat/chat.action'
import {DisplayUrls, DisplayWeather} from "./displayUrlsWeatherComponent";
import './chatbot.scss'

const Chatbot = ({chat, sendMessage, userMessage})=>{
    const [message, setMessage] = useState("")

    const endOfMessages = useRef(null)
    const element = document.getElementById("wrapper");
   
    const scrollToBottom = () => {
      console.log(endOfMessages)
      if(chat.length && endOfMessages.current){
        endOfMessages.current.scrollIntoView({ behavior: "smooth" })
      }
      
    }

    useEffect(scrollToBottom, [chat]);
    const handleClick = async (e) => {
        const code = e.keyCode || e.which;
    
        if (code === 13 && message) {
          userMessage({message: message, type: 'user'});
          //sendMessage(message);
          setMessage("");
        }
      };
    
      const displayMessage = (data, indx) =>{

        if (data.message){

          if (typeof data.message === 'string'){
            return <div className={data.type} key={indx}>{data.message}</div>
          }
          
          if (data.intent === 'GetWeather' && data.message.length){
            return (
              <div  className={data.type}>
                <DisplayWeather message={data.message}/>
              </div>
            )
          }

          return data.message.map((msg, indx) => (
            <div className={data.type} key={indx}>
              <div >{msg.title}</div>
              <div>{msg.description}</div>
              <DisplayUrls urls={msg.url}/>
            </div>
          ))
        }
       
      }
    return (
        <div className="chat">
          <div className="historyContainer">
          {chat.length === 0
          ? ""
          : chat.map(displayMessage)}
          </div>
           
            <input
                id="chatBox"
                onChange={(e) => setMessage(e.target.value)}
                onKeyPress={handleClick}
                value={message}
            ></input>
        </div>
    )
}

const mapStateToProps = (state, ownState)=>{

    return{
     chat: state.chat.query
    } 
  }

const mapDispatchToProps = (dispatch, ownProps) => {
    return {
      userMessage: (msg) => dispatch(chatActionStart(msg)),
      //sendMessage: (msg) => dispatch(chatActionSuccess(msg))
    }
  }

export default connect(mapStateToProps, mapDispatchToProps)(Chatbot)