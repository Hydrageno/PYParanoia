document.addEventListener("DOMContentLoaded", function(){
    /**
     * 绘画大字，即左下角的米字格中
     */
    const urlParams = new URLSearchParams(window.location.search);
    createChar(urlParams.get('tc'));
    function createChar(givenChar){
        var color = '#c41b14', size = 42; 
        var svg = d3.select(".giant-character").append("svg");
        svg.attr('width', "42vh").attr('height', "42vh");
        //内横线
        svg.append('line')
            .attr('x1',0)
            .attr('y1',String(size/2) + "vh")
            .attr('x2',String(size) + "vh")
            .attr('y2',String(size/2) + "vh")
            .attr('stroke',color)
            .attr('stroke-width', 1);
        //内竖线
        svg.append('line')
            .attr('x1',String(size/2) + "vh")
            .attr('y1',0)
            .attr('x2',String(size/2) + "vh")
            .attr('y2',String(size) + "vh")
            .attr('stroke',color)
            .attr('stroke-width', 1);
        //内斜线1
        svg.append('line')
            .attr('x1',0)
            .attr('y1',0)
            .attr('x2',String(size) + "vh")
            .attr('y2',String(size) + "vh")
            .attr('stroke',color)
            .attr('stroke-dasharray', '5,5')
            .attr('stroke-width', 1);
        //内斜线2
        svg.append('line')
            .attr('x1',0)
            .attr('y1',String(size) + "vh")
            .attr('x2',String(size) + "vh")
            .attr('y2',0)
            .attr('stroke',color)
            .attr('stroke-dasharray', '5,5')
            .attr('stroke-width', 1);
        //外框线
        svg.append('rect')
            .attr('fill','transparent')
            .attr('stroke',color)
            .attr('stroke-width', 5)
            .attr('x',0)
            .attr('y',0)
            .attr('width',String(size) + "vh")
            .attr('height',String(size) + "vh");
        //汉字
        svg.append('text')
            .attr('x',"4vh")
            .attr('y',String(size/2+10) + "vh")
            .style('font-size', '20rem')
            .style('font-family', 'Kaiti')
            .attr('fill','black')
            .text(givenChar);
    }

    /**
     * 从后端搜索当前字的具体信息
     */
    writeOnBlackboard(urlParams.get('tc'))
    function writeOnBlackboard(givenChar){
        fetch('http://127.0.0.1:5000/search_character_info/' + givenChar)
        .then(response => response.json())
        .then(data => {
            // 填写拼音
            var pinyin = document.querySelector('.pinyin-region');
            pinyin.innerHTML = `<span class="prefix">拼音：</span>${data['pinyin']}`;
            // 填写笔画
            var stroke_status = data['stroke_status']
            if(stroke_status == "FOUND")
            {
                var stroke = document.querySelector('.stroke-region');
                stroke.innerHTML = `<span class="prefix">笔画：</span>${data['stroke_info']}`;
            }
            // 填写词语及其解释
            var wtp_status = data['wtp_status']
            if(wtp_status == "FOUND")
            {
                var phrase = document.querySelector('.phrase-region');
                phrase.innerHTML = `<span class="prefix">词语：</span>${data['wtp_info']['word']}`;
                var phrase_pinyin = document.querySelector('.phrase-pinyin-region');
                phrase_pinyin.innerHTML = `<span class="prefix">词语拼音：</span>${data['wtp_info']['word_pinyin']}`;
                var explanation = document.querySelector('.phrase-explanation-region');
                explanation.innerHTML = `<span class="prefix">词语解释：</span>${data['wtp_info']['text']}`;
                var explanation_pinyin = document.querySelector('.phrase-explanation-pinyin-region');
                explanation_pinyin.innerHTML = `<span class="prefix">解释拼音：</span>${data['wtp_info']['text_pinyin']}`;
            }
            // 填写成语及其解释
            var idiom_status = data['idiom_status']
            if(idiom_status == "FOUND")
            {
                var idiom = document.querySelector('.idiom-region');
                idiom.innerHTML = `<span class="prefix">成语：</span>${data['idiom_info']['idiom']}`;
                var idiom_pinyin = document.querySelector('.idiom-pinyin-region');
                idiom_pinyin.innerHTML = `<span class="prefix">成语拼音：</span>${data['idiom_info']['idiom_pinyin']}`;
                var explanation = document.querySelector('.idiom-explanation-region');
                explanation.innerHTML = `<span class="prefix">成语解释：</span>${data['idiom_info']['explanation']}`;
                // var explanation_pinyin = document.querySelector('.phrase-explanation-pinyin-region');
                // explanation_pinyin.innerHTML = `词语拼音：${data['wtp_info']['text_pinyin']}`;
            }

        })
    }
})


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


function addWordbook()
{
    /**
     * 功能：添加至生词本
     */
    const urlParams = new URLSearchParams(window.location.search);
    fetch('http://127.0.0.1:5000/add_to_wordbook/' + urlParams.get('tc'))
    .then(response => response.json())
    .then(data => {
        console.log(data['message']);
        var cue = document.querySelector('.cue-region');
        cue.innerHTML = `已加入生词本！`;
    })
}


function backHome()
{
    /**
     * 功能：返回至主页面
     */
    window.location.href = './home.html';
}


function redirectWordbook()
{
    /**
     * 功能：前往生词本页面
     */
    window.location.href = './wordbook.html';
}