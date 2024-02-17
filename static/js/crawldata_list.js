window.onload = function() {
  const light_btn = document.getElementById("btnradio_ligth");
  const dark_btn = document.getElementById("btnradio_dark");
  const index_html = document.getElementById("index");
  const btn_reset = document.getElementById("btn_reset");
  const s_date = document.getElementById("s_date");
  const e_date = document.getElementById("e_date");
  const btn_load = document.getElementById("btn_load");
  const update_div = document.getElementById("update_div");
  const chk_all = document.getElementById("all-checkbox");
  const btn_del = document.getElementById("btn_del");

  const currentTheme = localStorage.getItem("theme");
  const last_update = localStorage.getItem("last_update");
  
  light_btn.addEventListener("click", function () {
    index_html.setAttribute("data-bs-theme", "light");
    let theme = "light";
    localStorage.setItem("theme", theme);
  });
  
  dark_btn.addEventListener("click", function () {
    index_html.setAttribute("data-bs-theme", "dark");
    let theme = "dark";
    localStorage.setItem("theme", theme);
  });
  
  if (currentTheme == "dark"){
    dark_btn.checked = true;
    index_html.setAttribute("data-bs-theme", "dark");
  } else if (currentTheme == "light") {
    light_btn.checked = true;
    index_html.setAttribute("data-bs-theme", "light");
  }
  
  // 필터 초기화 버튼을 누르면 폼안의 설정된 내용(주간사, 날짜) 를 처음 페이지 로딩 되었을 때의 값으로 변경
  btn_reset.addEventListener("click", function() {
    document.querySelectorAll("select[name=trading_firm_select] option")[0].selected = true;
    s_date.value = "";
    e_date.value = "";
  });
  
  chk_all.addEventListener('click', function() {
    const isChkd = chk_all.checked;
    if (isChkd) {
      const checkboxes = document.querySelectorAll('.chk');
      for(const checkbox of checkboxes){
        checkbox.checked = true;
      }
    }
    else {
      const checkboxes = document.querySelectorAll('.chk');
      for(const checkbox of checkboxes){
        checkbox.checked = false;
      }
    }
  });

  btn_del.addEventListener("click", function() {
    let isChkd = false
    const checkboxes = document.querySelectorAll('.chk');
    for(const checkbox of checkboxes){
      if (checkbox.checked){
        isChkd = checkbox.checked;
      }
    }
    if (isChkd){
      alert("선택한 항목을 정말 삭제 하시겠습니까?")
    } else {
      alert("선택된 항목이 없습니다. 삭제할 항목을 선택해 주세요.")
    }
  });
  
  // 최신 데이터 크롤링 버튼 클릭시 Django 와 비동기 처리 
  // 스피너 표현 해 주기 위해서 사용 근데 이게 맞나 ?, 멘토님 께 물어보기
  btn_load.addEventListener("click", function() {
    let btn_load = document.getElementById("btn_load");
    let spinner = document.getElementById("spinner_div");
  
    // ajax 에서 보내주는 값은 없고, 받는 값 만 있음
    // Django의 load_data 함수 실행 -> crawl_data() 실행 후 리턴 값 boolean 값으로 받아서 
    // 크롤링 잘 되었으면 true 반환 하게 했음 그래서 그 값을 json 형식으로 받아 콘솔에 출력, 전달 받은 값이 딱히 사용되는 곳은 없음
    $.ajax({
      url: "load_data",
      type: "GET",
      success: function(data) {
        let update_datetime = data.last_update['crawled_datetime'].replace('T', ' ');
        let split_datetime = update_datetime.split('.');
        localStorage.setItem("last_update", split_datetime[0]);
        update_div.innerHTML = split_datetime[0];
      },
      // crawl_data() 함수가 실행 될 동안 button 에 스피너 표현 하고 버튼 사용 할 수 없도록 disable 속성 부여
      beforeSend: function() {
        spinner.style.display = "block";
        btn_load.disabled = true;
      },
      // 실행 후 스피너는 안보이게하고 button 다시 작동 가능하게 원상 복구
      complete: function() {
        spinner.style.display = "none";
        btn_load.disabled = false;
      },
      error: function() {
        alert('안돼 돌아가');
      }
    });
  });
  
  update_div.innerHTML = last_update;
}