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