import { useState } from 'react'
import ship from '../src/assets/Player 1.png'
import './App.css'
import git from '../src/assets/github-seeklogo.svg'
import yt from '../src/assets/youtube-2017-seeklogo-2.svg'
import bg from '../src/assets/background.jpg'

function App() {
  const [count, setCount] = useState(0)

  return (
    <body>
      

      <img className="bg"src={bg} alt="" />  
      <img className="bg1"src={bg} alt="" />  
      <img className="bg2"src={bg} alt="" />  


    <><div>


      <div className='top'>
        <a href="" target="">
          <img src={ship} className="ship" alt="ship" />
        </a>
        <a href="https://youtu.be/mVVRqQ-QV0M" target='new'><img src={yt} alt="" className='yt'/> gameplay </a>
        <a href="https://github.com/Yan-Christian/Our-game" target="new">
          <img src={git} className="git"alt="" />
          repositório github
        </a>
      </div>
      <h1>Galatic Defenders!</h1>
      <h2>Seja um sobrevivente defensor da galáxia!!</h2>
      <form action="">
        <input type="name" name="" id="" placeholder='nome' />
        <input type="email" placeholder='email'/>
      </form>
      <div className="card">
        <button >
          COMPRE AGORA! 
        </button>
        <p>
          Disponível em 8 de Outubro
        </p>
      </div>
      <p className="read-the-docs">
        All rights reserved
      </p>
    </div>
    </>
    </body>
  )
}

export default App
