document.addEventListener("DOMContentLoaded", function(){
    /**
     * 请求生词内容，将生词内容显示在卷轴上
     */
    fetchAllWordbookContent();
    function fetchAllWordbookContent(){
        fetch('http://127.0.0.1:5000/compose_allwordbook/')
        .then(response => response.json())
        .then(data => {
            var wordbookContainer = document.querySelector('.wordbook-container');
            var contentTemplate = document.createElement('div');
            contentTemplate.classList.add('content-template');
            contentTemplate.innerHTML = `
                <div class="template-theme">生字本：</div>
                <div class="template-content">${data['wordbook']}</div>
                <br>
            `
            wordbookContainer.appendChild(contentTemplate);
            console.log(data['gradewordbook'])
            for (const [key, value] of Object.entries(data['gradewordbook'])) {
                var contentTemplate = document.createElement('div');
                contentTemplate.classList.add('content-template');
                contentTemplate.innerHTML = `
                    <div class="template-theme">${key}</div>
                    <div class="template-content">${value}</div>
                    <br>
               `
               wordbookContainer.appendChild(contentTemplate);
            }
        })
    }
})


function backHome()
{
    /**
     * 功能：返回至主页面
     */
    window.location.href = './home.html';
}


function redirectWordbookExamine()
{
    /**
     * 功能：重定位至练习页面
     */
    window.location.href = './examine.html';
}


function redirectPhrase()
{
    /**
     * 功能：重定位至练习页面
     */
    window.location.href = './phrase.html';
}