import './App.css'

const menu=['Dashboard','Platform','Users','Analytics','Monitoring','Settings']
const cards=[['전체 회원','24,581'],['오늘 접속','8,942'],['처리 주문','1,284'],['시스템 상태','99.9%']]

export default function App(){
 return <div className="layout">
  <aside className="side"><h1>DAEJUNG<br/>NEXT</h1>{menu.map((m,i)=><div className={i===0?'on':''}>{m}</div>)}</aside>
  <main className="main">
   <header><div><small>CORE SYSTEM</small><h2>Platform Dashboard</h2></div><button>Admin</button></header>
   <section className="steps"><span>01 Setup</span><span>02 Data</span><span>03 Manage</span><span>04 Monitor</span></section>
   <section className="cards">{cards.map(c=><article><p>{c[0]}</p><b>{c[1]}</b></article>)}</section>
   <section className="grid"><div className="panel"><h3>Platform Overview</h3><div className="chart"></div></div><div className="panel"><h3>System Activity</h3><p>회원 데이터 동기화 완료</p><p>주문 처리 엔진 정상</p><p>서비스 상태 정상</p></div></section>
   <section className="panel table"><h3>Recent Operations</h3><div>CORE 운영 로그 / 관리자 작업 기록</div></section>
  </main>
 </div>
}
