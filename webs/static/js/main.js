async function post_to_ai(){
    var input_box = document.getElementById("ipt")
    var ipt = input_box.value
    var parent = document.getElementById("message-box");
    var new_para = document.createElement("p");
    var node = document.createTextNode('USER: '+ipt)
    var button = document.getElementById("post-button");
    button.disabled = true
    button.textContent = 'AI回答中';
    input_box.value = ''
    new_para.appendChild(node)
    parent.appendChild(new_para)
    var response = await fetch("/api/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            query: ipt,
        })
    })
    var data = await response.json()
    node = document.createTextNode('AI: '+data.message);
    new_para = document.createElement("p");
    new_para.appendChild(node)
    parent.appendChild(new_para)
    button.textContent = '发送'
    button.disabled = false
}


async function change_client() {
    var api_key = document.getElementById("api_key").value;
    var base_url = document.getElementById("base_url").value;
    var model_name = document.getElementById("model_name").value;

    await fetch('/api/change_client', {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                api_key: api_key,
                base_url: base_url,
                model_name: model_name,
            })
        }
    )
}
