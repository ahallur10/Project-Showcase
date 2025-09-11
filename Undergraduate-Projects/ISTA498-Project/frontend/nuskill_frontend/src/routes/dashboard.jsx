import React, { useEffect,useState }  from 'react'
import { Layout } from '../components/layout'
import { Article, ArticleContent, ArticleMedia } from '../components/article'
import HorizontalScroll from 'react-horizontal-scrolling'
import {Navigate, useNavigate} from 'react-router-dom';

export default function DashboardPage() {
  const [value, setValue] = useState('5');
  const [earnedBack, setearnedBack] = useState(0);
  const [toEarn, setToEarn] = useState(40);
  const [checksComp, setchecksComp] = useState(0);
  const [checks, setChecks] = useState(80);

  const [deposited, setDeposited] = useState(false);
  const [videoShow, setVideoShow] = useState(false);
  const nav = useNavigate()

  function randomNumberInRange(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  }

  function getDepositURLandRedirect(e) {
    fetch('http://localhost:8080/payment/deposit',{method: 'POST',  headers: {'content-type': 'application/json'},
          body: JSON.stringify({"id":'new_user_5',"amount":'40'})
    }).then(async (res)=>
        
    {res = await res.json();setDeposited(true);window.localStorage.setItem('deposited',true);window.location.href = res.body;})

  }
  useEffect(() => {
    if (window.localStorage.getItem('deposited') == 'true'){

      setDeposited(true);
    }

  }, []);
  
  return (
    <Layout>
      <Article>
        <ArticleContent title="Dashboard">
          {deposited === false? 
            <><p>It seems you haven't deposited for today. Make a deposit to access NuSkill Resources.</p><input type="range" onChange={(event) => setValue(event.target.value.toString())} value={value} step="1" min="0" max="100" /><text>&nbsp;${value}</text>
            &nbsp;&nbsp;&nbsp;&nbsp;
            <button
            className="-mt-px inline-flex cursor-pointer justify-center whitespace-nowrap rounded-sm border-0 bg-gradient-to-r from-secondary-500 to-secondary-400 py-4 px-7 text-center font-medium leading-4 text-white no-underline shadow-lg"
            onClick={getDepositURLandRedirect}
            >
            {'Deposit'}
            </button> </>:
            <>
            <ArticleContent> <p>${earnedBack}/{toEarn} {checksComp}/{checks} </p></ArticleContent>

            <HorizontalScroll>
              <div>
                  
              <iframe
            width="400"
            height="245"
            src={'https://www.youtube.com/embed/Xe-C4lEPyC4'}
            frameBorder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            title="Embedded youtube"
            onClick={(e)=>nav('/video')}
          />
           <iframe
            width="400"
            height="245"
            src={'https://www.youtube.com/embed/Dex5BvyR5cA'}
            frameBorder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
            title="Embedded youtube"
            onClick={(e)=>setVideoShow(true)}
          /> 
          <iframe
            width="400"
            height="245"
            src={'https://www.youtube.com/embed/Uq1KzvzsRLA'}
            frameBorder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
            title="Embedded youtube"
            onClick={(e)=>setVideoShow(true)}
          /> 
           <iframe
            width="400"
            height="245"
            src={'https://www.youtube.com/embed/PNqTd-YpbRU'}
            frameBorder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
            title="Embedded youtube"
            onClick={(e)=>setVideoShow(true)}
          /> 
           <iframe
            width="400"
            height="245"
            src={'https://www.youtube.com/embed/9F6JkpokVq0'}
            frameBorder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
            title="Embedded youtube"
            onClick={(e)=>setVideoShow(true)}
          /> 
          </div>

              
            </HorizontalScroll >
                 
            </>}
            
          </ArticleContent>
        <ArticleMedia>
        {deposited === false? <img src='../assets/nuskillimage2.JPG' alt='image' width="600em"/>:<img src='../assets/nuskillpic1.JPG' alt='image' width="600em"/>}
            

        </ArticleMedia>
      </Article>
    </Layout>
  )
}
