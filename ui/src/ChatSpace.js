import './ChatSpace.css';
import logo from './unbxd-logo.png';
import send from './send.png';
import voice from './voice.png';
import upload from './upload-image.png';
import { useState } from 'react';
import { Swiper, SwiperSlide } from 'swiper/react';
import { Navigation, Pagination, Scrollbar, A11y, EffectCube } from 'swiper';
import 'swiper/swiper-bundle.min.css';
import axios from 'axios';

function Chat() {

    const [question, setQuestion] = useState('');

    const [history, setHistory] = useState([{key: 1, ai: true, text: 'How may I help you ?', initial: true, filters: [], products: [], auto: [] }]);

    const [typing, setTyping] = useState(false);

    const showTime = new Date().toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true });

    const handleKeyDown = (event) => {
        if (event.key === 'Enter') {
          handleClickSend();
        }
      }

      const handleClickSend = () => {

        setTyping(true);

        const data = {
            text: question,
            convo_id:"123"
        }
        
        axios.post("http://192.168.2.150:8080/sites/express-1233/chatbot?uid=12", data )
            .then((response) => {
                setHistory((current) => ([...current, {key:3, ai:true, text:response.data.response.text, filters: response.data.response.filter, products: response.data.response.products, auto: response.data.response.autosuggest}]));
                setTyping(false);
             })
            .catch((err) => {
                //   this.setState({ data: err, isLoading: false });
             });
        
        setHistory((current) => ([...current, {key:2,ai:false,text:question}]));
        setQuestion('')
      }

      const resultHistory = history.map((val, i) => {
      
        if (val.ai === true) {
            return (
             <div className='outer-sectionAI'>
                {!val.initial && <div className='carousel-wrapper'> 
                            <Swiper
                                modules={[Navigation, Pagination, Scrollbar, A11y, EffectCube]}
                                spaceBetween={20}
                                slidesPerView={5}
                                onSlideChange={() => console.log('slide change')}
                                onSwiper={(swiper) => console.log(swiper)}
                                navigation={{ clickable: true }}
                                >
                                {val.products && val.products.map((e, i) => {
                                    return(
                                <SwiperSlide>
                                 <div id={e.productId}>
                                    <img src={e.image_url} alt={e.title} className='swiper-image'></img>
                                     <p className="title">{e.title}</p>
                                     <p className='last-price'>₹ {e.last_price}</p>
                                     <p className='sale-price'>₹ {e.sale_price}</p>
                                </div>
                             </SwiperSlide>
                                    )
                                }) }
                            </Swiper>
                </div>}
                <div className="sectionBallonAi">
                    <div className="ballon ai">{val.text}</div>
                </div>
                { !val.initial && <div className='filter-section'>
                    {val.filters && val.filters.map((e, i) => {
                        return (
                            <div className="filter-options" key={i} onClick={() =>  setQuestion(e)}>
                                {e}
                        </div>
                    );
                })}
             </div> 
            }
            { !val.initial && <div className='filter-section'>
                    {val.auto && val.auto.map((e, i) => {
                        return (
                            <div className="filter-options auto" key={i} onClick={() =>  setQuestion(e)}>
                                {e}
                        </div>
                    );
                })}
             </div> 
            }
             </div>   
            );
        } 
        else {
          return (
            <div className="sectionBallonHuman" key={i}>
              <div className="ballon human">{val.text}</div>
            </div>
          );
        }
      });

    return(
        <div className="chat">
            <div className="contact bar">
                <img src={logo} alt='logo' className='logo'></img>
                <div className="name">
                    Unbxd Shopping Assistant
                </div>
            </div>
            <div className="messages" id="chat">
                <div className="time">
                    Today at {showTime}
                </div>
            <div className=''>{resultHistory}</div>   
            {typing && <div className="message stark">
                <div className="typing typing-1"></div>
                <div className="typing typing-2"></div>
                <div className="typing typing-3"></div>
            </div>}
            </div>    
        <div className="input">
          <i className="fas fa-camera"></i><i className="far fa-laugh-beam"></i><input className="input" type="text" value={question} onChange={e => setQuestion(e.target.value)} onKeyDown={handleKeyDown} placeholder="Type your message here!" ></input>
          <img src={voice} alt="send" onClick={handleClickSend} className='voice'></img>
          <img src={upload} alt="send" onClick={handleClickSend} className='upload'></img>
          <img src={send} alt="send" onClick={handleClickSend} className='send'></img>
        <i className="fas fa-microphone"></i>
        </div>
      </div> 
    )
}

export default Chat;