const hamMenu = document.querySelector('.ham-menu');
const offScreenMenu = document.querySelector('.off-screen-menu');
let previousScrollY = window.scrollY;

hamMenu.addEventListener('click', () => {
    hamMenu.classList.toggle('active');
    offScreenMenu.classList.toggle('active');
});

window.addEventListener('scroll', () => {
    if (offScreenMenu.classList.contains('active')) {
        offScreenMenu.classList.remove('active');
        hamMenu.classList.remove('active');
    }
});
