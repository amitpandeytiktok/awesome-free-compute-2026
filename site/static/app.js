// Close the mobile nav after tapping a link.
document.querySelectorAll('.mainnav a').forEach(a=>{
  a.addEventListener('click',()=>document.body.classList.remove('nav-open'));
});

// Live crypto price chips in the ticker — keyless CoinGecko, progressive enhancement.
(function(){
  var groups = document.querySelectorAll('.ticker-group');
  if(!groups.length) return;
  var COINS = [['bitcoin','BTC'],['ethereum','ETH'],['solana','SOL'],['binancecoin','BNB'],['dogecoin','DOGE']];
  var ids = COINS.map(function(c){return c[0];}).join(',');
  var url = 'https://api.coingecko.com/api/v3/simple/price?ids='+ids+'&vs_currencies=usd&include_24hr_change=true';
  function price(n){
    return n>=1 ? '$'+n.toLocaleString('en-US',{maximumFractionDigits:n>=1000?0:2})
                : '$'+n.toLocaleString('en-US',{maximumFractionDigits:4});
  }
  function render(data){
    var html='';
    COINS.forEach(function(c){
      var d=data[c[0]]; if(!d||d.usd==null) return;
      var ch=d.usd_24h_change||0, up=ch>=0;
      html += '<a class="ti ti-px ti-crypto" href="https://www.coingecko.com/en/coins/'+c[0]+
              '" target="_blank" rel="noopener"><span class="sym">'+c[1]+'</span> '+price(d.usd)+
              ' <span class="chg '+(up?'up':'down')+'">'+(up?'▲':'▼')+Math.abs(ch).toFixed(1)+'%</span></a>';
    });
    if(!html) return;
    groups.forEach(function(g){
      g.querySelectorAll('.ti-px').forEach(function(e){e.remove();});
      g.insertAdjacentHTML('afterbegin', html);
    });
  }
  function load(){
    fetch(url,{cache:'no-store'})
      .then(function(r){return r.ok?r.json():null;})
      .then(function(d){if(d)render(d);})
      .catch(function(){});
  }
  load();
  setInterval(load, 60000);
})();

