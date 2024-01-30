/**
 * AUTHOR NAME: Tsung Yilee
 * AUTHOR EMAIL: свит_дрим@yandex.com
 */
var question_nums = 0;
document.addEventListener("DOMContentLoaded", function(){
    /**
     * 初始化部分按钮的样式，最初时候不能提交也不能下载
     */
    var downloadAnalysisButton = document.querySelector('.download-analysis');
    downloadAnalysisButton.disabled = true;
    downloadAnalysisButton.style.cursor = 'not-allowed';
    var submitAnswersButton = document.querySelector('.submit-answers');
    submitAnswersButton.disabled = true;
    submitAnswersButton.style.cursor = 'not-allowed';
})


function backHome(){
    /**
     * 功能：返回至主页面
     */
    window.location.href = './home.html';
}


function fetchGradewordbookQuestions(){
    /**
     * 用以获取不同年级不同时期的题目
     */
    // 首先需要获取用户的选择
    var gradePeriodRankSelectResult = document.getElementById('gradePeriodRankSelect').value;
    var hyperModeSelectResult = document.getElementById('hyperModeSelect').value;
    var settingToSend = {
        "mode": "gradewordbook",
        "gradeperiod": gradePeriodRankSelectResult,
        "hybrid_mode": hyperModeSelectResult
    };
    var settingJSON = JSON.stringify(settingToSend);
    fetchQuestions(settingJSON);
}


function fetchWordbookQuestions(){
    /**
     * 用以获取基于生字本的题目
     */
    var settingToSend = {
        "mode": "wordbook",
    };
    var settingJSON = JSON.stringify(settingToSend);
    fetchQuestions(settingJSON);
}


function fetchQuestions(settingJSON){
        // 使用 fetch 发送 POST 请求给服务器
        fetch('http://127.0.0.1:5000/fetch_questions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: settingJSON,
        })
        .then(response => response.json())
        .then(data => {
            var questionContainer = document.querySelector('.questions-container');
            var questions = data['questions'];
            question_nums = questions.length;
            questionContainer.innerHTML = '';
            for(var i = 0; i < questions.length; i++)
            {
                var question = questions[i];
                var questionTemplate = document.createElement('div');
                questionTemplate.classList.add('question-template');
                questionTemplate.innerHTML = `
                    第（<span class="question-id prefix">${question.question_id}</span>）题
                    <br>
                    <span class="prefix">题干</span>：
                    <span class="question-maintext">${question.question_maintext}</span>
                    <br>
                    <span class="prefix">提示</span>：
                    <span class="question-desc">${question.question_desc}</span>
                    <br>
                    <label for="q${question.question_id}"><span class="prefix">作答</span>：</label>
                    <input type="text" class="question-reply" id="q${question.question_id}">
                    <span class="response-template" id="r${question.question_id}"></span>
                    <br>
                    <br>
                `;
                questionContainer.appendChild(questionTemplate);
            }
            // 获取到题目开放提交，但是任然锁定下载
            var submitAnswersButton = document.querySelector('.submit-answers');
            submitAnswersButton.disabled = false;
            submitAnswersButton.style.cursor = 'pointer';
            var downloadAnalysisButton = document.querySelector('.download-analysis');
            downloadAnalysisButton.disabled = true;
            downloadAnalysisButton.style.cursor = 'not-allowed';
        })
}


function finishQuestions(){
    // 提交后禁止重复提交
    var submitAnswersButton = document.querySelector('.submit-answers');
    submitAnswersButton.disabled = true;
    submitAnswersButton.style.cursor = 'not-allowed';
    var user_answers = [];
    for(var i = 1; i <= question_nums; i++)
    {
        var questionReply = document.getElementById('q' + String(i));
        user_answers.push(questionReply.value);
    }
    var userAnswersToSend = {
        "user_answers": user_answers
    };
    var userAnswerJSON = JSON.stringify(userAnswersToSend);
    // 使用 fetch 发送 POST 请求给服务器
    fetch('http://127.0.0.1:5000/process_uanswer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: userAnswerJSON,
    })
    .then(response => response.json())
    .then(data => {
        for(var i = 0; i < data['response'].length; i++){
            var response = data['response'][i]
            var repsonseTemplate = document.getElementById('r' + String(i + 1));
            var innerContent = document.createElement('span');
            if(response['message'] == '回答错误'){
                innerContent.innerHTML = `
                <span class="response-message">${response['message']}</span>
                <span class="response-prefix">&nbsp;&nbsp;答案：</span>
                <span class="response-answer">${response['answer']}</span>
                `
            }
            else{
                innerContent.innerHTML = `
                <span class="response-message">${response['message']}</span>
                `
            }
            repsonseTemplate.appendChild(innerContent)
        }
        //提交后允许下载分析结果
        var downloadAnalysisButton = document.querySelector('.download-analysis');
        downloadAnalysisButton.disabled = false;
        downloadAnalysisButton.style.cursor = 'pointer';
    })
}