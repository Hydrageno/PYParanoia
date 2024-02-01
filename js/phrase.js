/**
 * AUTHOR NAME: Tsung Yilee
 * AUTHOR EMAIL: свит_дрим@yandex.com
 */
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
                    <div class="word">
                        <span class="prefix">词语：</span>
                        ${data['words'][i]}
                    </div>
                    <div class="word-pinyin">
                        <span class="prefix">拼音：</span>
                        ${data['words_pinyin'][i]}
                        <span class="hidden-content">${data['words'][i]}</span>
                        <button type="button" class="machine-read-button" title="念出来" onclick="machineRead(event)">念</button>
                    </div>
                    <div class="text">
                        <span class="prefix">词语解释：</span>
                        ${data['texts'][i]}
                    </div>
                    <div class="text-pinyin">
                        <span class="prefix">解释拼音：</span>
                        ${data['texts_pinyin'][i]}
                        <span class="hidden-content">${data['texts'][i]}</span>
                        <button type="button" class="machine-read-button" title="念出来" onclick="machineRead(event)">念</button>
                    </div>
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


var backEndSpeaked = false; // 阻止一次性过多访问，导致崩溃
function machineRead(event)
{
    /**
     * 功能：念出来！
     */
    if(backEndSpeaked == true)return;
    backEndSpeaked = true;
    var button = event.target;
    var previousSibling = button.previousElementSibling; // 使用 previousElementSibling 获取前一个兄弟元素节点
    previousSibling.style.display = 'inline'; // 将前一个兄弟元素节点显示出来
    fetch('http://127.0.0.1:5000/machine_read/' + previousSibling.textContent)
    .then(response => response.json())
    .then(data => {
        console.log(data['message']);
        backEndSpeaked = false; //直至后端念完后，才允许下一个点击
    })
    previousSibling.style.display = 'none'; // 恢复前一个兄弟元素节点的隐藏状态
}
