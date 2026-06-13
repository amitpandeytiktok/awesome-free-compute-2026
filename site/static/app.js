// Close the mobile nav after tapping a link.
document.querySelectorAll('.mainnav a').forEach(a=>{
  a.addEventListener('click',()=>document.body.classList.remove('nav-open'));
});
