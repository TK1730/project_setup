// 共通クイズ部品。
// 使い方:
//   <div class="quiz" data-answer="2" data-explain="解説文">
//     <div class="q">問題文</div>
//     <div class="opts"><button class="opt">A</button>...</div>
//   </div>
// data-answer は 0 始まりの正解の位置。ページ内に .quiz-score があれば得点を表示する。
(function () {
  const quizzes = Array.from(document.querySelectorAll(".quiz"));
  let answered = 0, correct = 0;

  function updateScore() {
    document.querySelectorAll(".quiz-score").forEach((el) => {
      el.textContent = `${answered} / ${quizzes.length} 問回答・正解 ${correct}`;
    });
  }

  quizzes.forEach((quiz) => {
    const answer = Number(quiz.dataset.answer);
    const opts = Array.from(quiz.querySelectorAll("button.opt"));
    const fb = document.createElement("div");
    fb.className = "fb";
    quiz.appendChild(fb);

    opts.forEach((btn, i) => {
      btn.type = "button";
      btn.addEventListener("click", () => {
        opts.forEach((b) => (b.disabled = true));
        opts[answer].classList.add("correct");
        const ok = i === answer;
        if (!ok) btn.classList.add("wrong");
        answered += 1;
        if (ok) correct += 1;
        fb.innerHTML = `<span class="verdict">${ok ? "正解。" : "不正解。"}</span> ${quiz.dataset.explain || ""}`;
        fb.classList.add("show");
        updateScore();
      });
    });
  });
  updateScore();
})();
