'use strict;'

//la funzione viene chiamata ogni volta che scrivo qualcosa nella casella di testo
document.querySelector('section > .search').addEventListener('change', e => {
    e.preventDefault();
    const filter = document.querySelector('section > .search').value;
    const articles = document.querySelectorAll('.articles');
    for (let article of articles) {
        //visualizzo il filtro dalla console
        console.log(filter)
        //visualizzo i nomi dei titoli
        console.log(article.querySelector('.tag_title > a').text)

        if(filter !== "" && filter !== article.querySelector('.tag_title > a').text) {
            article.classList.add('hide');
        } else {
            article.classList.remove('hide');
        }
    }
});

/*
document.querySelectorAll('section > a').forEach(link =>{
    link.addEventListener('click', e => {
        e.preventDefault();
        const filter = e.target.dataset.tag;
        const articles = document.querySelectorAll('.articles');
        for (let article of articles) {
            if(filter !== article.querySelector('.tag_title > a').text) {
                article.classList.add('hide');
            }
        }
    });
});
 */