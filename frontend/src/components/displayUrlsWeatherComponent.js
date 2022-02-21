export const DisplayUrls = ({urls})=>{
    return urls.map((url, indx) =>(
      <div key={indx}>
        <a href={url}>link</a>
      </div>
    ))
  }

export const DisplayWeather = ({message})=>{
    return message.map((msg, indx) => (
      <div key={indx}>
        <div >Temperature: {msg.temperature}</div>
        <div>Humidity: {msg.humidity}</div>
        <div>Wind: {msg.wind}</div>
      </div>
    ))
  }

