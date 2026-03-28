let role = "student";

let notices = JSON.parse(localStorage.getItem("notices")) || [
    {title:"Mid-Term Exam", category:"Exam", desc:"Schedule released"},
    {title:"Tech Fest", category:"Event", desc:"Registration open"},
    {title:"Placement Drive", category:"Placement", desc:"Tech Corp hiring"}
];

function setRole(r){
    role = r;
}

function login(){
    if(role === "admin"){
        window.location.href = "admin.html";
    } else {
        window.location.href = "dashboard.html";
    }
}

function logout(){
    window.location.href = "index.html";
}

function displayNotices(list){
    let div = document.getElementById("notices");
    if(!div) return;

    div.innerHTML = "";
    list.forEach(n => {
        div.innerHTML += `
        <div class="notice">
            <h3>${n.title}</h3>
            <p>${n.category}</p>
            <p>${n.desc}</p>
        </div>`;
    });
}

function searchNotice(){
    let val = document.getElementById("search").value.toLowerCase();
    let filtered = notices.filter(n => n.title.toLowerCase().includes(val));
    displayNotices(filtered);
}

function filter(cat){
    if(cat === "all"){
        displayNotices(notices);
    } else {
        displayNotices(notices.filter(n => n.category === cat));
    }
}

function addNotice(){
    let t = document.getElementById("title").value;
    let c = document.getElementById("category").value;
    let d = document.getElementById("desc").value;

    notices.push({title:t, category:c, desc:d});
    localStorage.setItem("notices", JSON.stringify(notices));

    alert("Notice Added!");
    location.reload();
}

function loadAdmin(){
    let div = document.getElementById("adminNotices");
    if(!div) return;

    div.innerHTML = "";
    notices.forEach(n => {
        div.innerHTML += `<p>${n.title} - ${n.category}</p>`;
    });
}

displayNotices(notices);
loadAdmin();