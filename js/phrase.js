function searchPhrase(){
    /**
     * 功能：搜索给定固定格式词语
     */
    var searchBar = document.getElementById("searchBar");
    var searchBarValue = searchBar.value;
    if(searchBarValue.trim().length == 0)
    {
        searchBar.placeholder = "请输入格式再进行检索哦"
        return;
    }
    // 将目标集合转换为 Set
    const targetCategory = new Set(['AABB', 'ABAB', 'ABAC', 'ABB', 'ABCC', 'AAB', 'ABCA', 'ABCB', 'ABBC', 'AABC', 'AA', 'A里AB']);
    // 将 searchBarValue 转换为小写，使大小写不敏感->检查转换后的值是否在目标集合中
    if(targetCategory.has(searchBarValue.toUpperCase()) == false){
        searchBar.value = ""
        searchBar.placeholder = "请输入正确格式再进行检索哦"
        return;
    }
    else{
        fetch('http://127.0.0.1:5000/search_ffp_info/' + searchBarValue)
        .then(response => response.json())
        .then(data => {
            var writableRegion = document.querySelector('.writable-region');
            for(let i = 0; i < data['words'].length; i++){
                var contentTemplate = document.createElement('div');
                contentTemplate.classList.add('content-template');
                contentTemplate.innerHTML = `
                    <div class="word"><span class="prefix">词语：</span>${data['words'][i]}</div>
                    <div class="word-pinyin"><span class="prefix">拼音：</span>${data['words_pinyin'][i]}</div>
                    <div class="text"><span class="prefix">词语解释：</span>${data['texts'][i]}</div>
                    <div class="text-pinyin"><span class="prefix">解释拼音：</span>${data['texts_pinyin'][i]}</div>
                    <br>
                `
                writableRegion.appendChild(contentTemplate);
            }
        })
    }
}


function backHome(){
    /**
     * 功能：返回至主页面
     */
        window.location.href = './home.html';
}


function redirectWordbook()
{
    /**
     * 功能：重定位至练习页面
     */
    window.location.href = './wordbook.html';
}


function redirectWordbookExamine()
{
    /**
     * 功能：重定位至练习页面
     */
    window.location.href = './examine.html';
}

