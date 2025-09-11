import React, { useEffect,useState }  from 'react'
import { Layout } from '../components/layout'
import { Article, ArticleContent, ArticleMedia } from '../components/article'
import HorizontalScroll from 'react-horizontal-scrolling'

export default function VideoPage() {
  const [value, setValue] = useState('5');
  const [deposited, setDeposited] = useState(true);
  const [videoShow, setVideoShow] = useState(false);
  const [alert, setAlert] = useState(false);
  const [earnedBack, setearnedBack] = useState(0);
  const [toEarn, setToEarn] = useState(40);
  const [checksComp, setchecksComp] = useState(0);
  const [checks, setChecks] = useState(80);
  const [progress, setProgress] = useState(0)
  function randomNumberInRange(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  }
  
  const MINUTE_MS = 2000;

  function check() {
    if (progress < 5){
      setProgress(progress + 1);
      setearnedBack(earnedBack+ .50)
      setchecksComp(checksComp+1)
    }
  }
  
  // Write this line
  useEffect(() => {
   
    }, []);
  
  
   setTimeout(() => {
      check();
     }, 60000);
  
  return (
    <Layout>
      <Article>
        <ArticleContent title="Video">
          <ArticleContent> <p>${earnedBack}/{toEarn} {checksComp}/{checks} </p></ArticleContent>

            <iframe
            width="850"
            height="500"
            src={'https://www.youtube.com/embed/Xe-C4lEPyC4'}
            frameBorder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
            title="Embedded youtube"
          />
           <progress className="progressBar" value={progress.toString()} max="5">  </progress>
           <text>{progress}/5</text>
       
          </ArticleContent>
        <ArticleMedia>

        </ArticleMedia>
      </Article>
    </Layout>
  )
}
