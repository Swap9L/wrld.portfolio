let bg = document.getElementById('bg');
let home = document.getElementById('home');
let hambugger = document.getElementById('hambugger');
let closeBtn = document.getElementById('closeBtn');
let nav = document.getElementById('nav');
let logo = document.getElementById('logo');
let menuText = document.getElementById('menuText');
let changeText = document.getElementById('change');

/*window.addEventListener('scroll', function(){
    if(window.innerHeight < 850){
        bg.style.backgroundPositionY = -window.pageYOffset+'px';
    }    
    if (window.pageYOffset >20) {
        logo.style.opacity = "0";
        menuText.style.opacity = "0";    
    }
    else{
        logo.style.opacity = "1";
        menuText.style.opacity = "1";    
    }

})*/

string1 = "Get Your Portfolio . . !";
string2 = "Visit Us..!";
string3 = "Follow Us..!";
i = 0;
j = 0;
k = 0;
window.addEventListener('load', ()=>{
    typewriter();
    
})

async function typewriter(){
    if(i< string1.length){
        changeText.innerHTML =  changeText.innerHTML + string1.charAt(i);
        i++;
        setTimeout(typewriter, 200);
    }
    else{
        changeText.innerHTML = "";
        j = 0;
        typewriter2();
    }
}

async function typewriter2(){
    if(j< string2.length){
        changeText.innerHTML =  changeText.innerHTML + string2.charAt(j);
        j++;
        setTimeout(typewriter2, 200);
    }
    else{
        changeText.innerHTML = "";
        k = 0;
        typewriter3();
    }
}

async function typewriter3(){
    if(k< string3.length){
        changeText.innerHTML =  changeText.innerHTML + string3.charAt(k);
        k++;
        setTimeout(typewriter3, 200);
    }
    else{
        changeText.innerHTML = "";
        i = 0;
        typewriter();
    }
}

//  // Get all "show more" buttons
//  const showMoreButtons = document.querySelectorAll(".show-more");

//  // Add click event listeners to each button
//  showMoreButtons.forEach((button) => {
//    button.addEventListener("click", () => {
//      // Get the parent card element
//      const card = button.parentElement.parentElement;

//      // Toggle the "show" class on the card element
//      card.classList.toggle("show");
//    });
//  });

hambugger.addEventListener('click', ()=>{
    nav.style.opacity = "1";
    nav.style.visibility = "visible";
    nav.style.transform = "translateX(-270px)";
    nav.style.transition = "all 0.4s ease-in-out";
    nav.style.zIndex = "999";
})

closeBtn.addEventListener('click',()=>{
    nav.style.opacity = "0";
    nav.style.visibility = "hidden";
    nav.style.transform = "translateX(270px)";
    nav.style.transition = "all 0.4s ease-in-out";
    nav.style.zIndex = "999";
})



