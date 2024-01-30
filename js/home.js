function setTargetCharacter(){
    /**
     * 功能：设置后端目标关键字
     */
    var searchBar = document.getElementById("searchBar");
    var searchBarValue = searchBar.value;
    if(searchBarValue.trim().length == 0)
    {
        searchBar.placeholder = "请输入汉字再进行检索哦"
        return;
    }
    else if(searchBarValue.trim().length > 1)
    {
        searchBar.value = ""
        searchBar.placeholder = "请只输入一个汉字哦"
        return;                    
    }
    fetch('http://127.0.0.1:5000/set_target_character/' + searchBarValue)
    .then(response => response.json())
    .then(data => {
        console.log(data['message']);
        const params = new URLSearchParams({
            'tc': searchBarValue
        });
        window.location.href = './character.html?' + params.toString();
    })
}


document.addEventListener("DOMContentLoaded", function(){
    /**
     * 为下方介绍卡片添加点击跳转事件
     */
    var characterCard = document.querySelector('.character-card');
    characterCard.addEventListener('click', function() {
        // 无，这里本来就希望用户通过搜字跳转查字页面，而非随意查
    });
    var wordbookCard = document.querySelector('.wordbook-card');
    wordbookCard.addEventListener('click', function() {
        window.location.href = './wordbook.html';
    })
    var examineCard = document.querySelector('.examine-card');
    examineCard.addEventListener('click', function() {
        window.location.href = './examine.html';
    })
    var phraseCard = document.querySelector('.phrase-card');
    phraseCard.addEventListener('click', function() {
        window.location.href = './phrase.html';
    })
})