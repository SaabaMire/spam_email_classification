const form = document.querySelector("#prediction-form");
const messageInput = document.querySelector("#message");
const count = document.querySelector("#character-count");
const result = document.querySelector("#result");
const errorBox = document.querySelector("#error-message");
const submitButton = form.querySelector("button[type='submit']");

let browserModel;

const examples = {
  spam: "URGENT! You have won a free cash prize. Click this link now to claim your reward before it expires!",
  ham: "Hi, can we move tomorrow's team meeting to 10:30 in the morning? Please let me know if that works.",
};

const modelReady = fetch("model.json")
  .then((response) => {
    if (!response.ok) throw new Error("The classification model could not be loaded.");
    return response.json();
  })
  .then((data) => {
    browserModel = data;
    return data;
  });

messageInput.addEventListener("input", () => {
  count.textContent = `${messageInput.value.length.toLocaleString()} / 5,000`;
});

document.querySelectorAll("[data-example]").forEach((button) => {
  button.addEventListener("click", () => {
    messageInput.value = examples[button.dataset.example];
    messageInput.dispatchEvent(new Event("input"));
    messageInput.focus();
  });
});

function classifyMessage(message) {
  const cleaned = message.toLowerCase().replace(/[^a-z\s]/g, " ");
  const tokens = cleaned.match(/\b[a-z]{2,}\b/g) || [];
  const counts = new Map();

  for (const token of tokens) {
    const index = browserModel.vocabulary[token];
    if (index !== undefined) counts.set(index, (counts.get(index) || 0) + 1);
  }

  let normSquared = 0;
  const weightedTerms = [];
  for (const [index, frequency] of counts) {
    const weight = frequency * browserModel.idf[index];
    weightedTerms.push([index, weight]);
    normSquared += weight * weight;
  }

  const norm = Math.sqrt(normSquared) || 1;
  let decision = browserModel.intercept;
  for (const [index, weight] of weightedTerms) {
    decision += browserModel.coefficients[index] * (weight / norm);
  }

  const hamProbability = 1 / (1 + Math.exp(-decision));
  const spamProbability = 1 - hamProbability;
  const isSpam = spamProbability > hamProbability;

  return {
    label: isSpam ? "spam" : "ham",
    display_label: isSpam ? "Spam" : "Not spam",
    confidence: Math.max(spamProbability, hamProbability) * 100,
    spam_probability: spamProbability * 100,
    ham_probability: hamProbability * 100,
  };
}

function showResult(data) {
  const isSpam = data.label === "spam";
  result.className = `result visible ${isSpam ? "spam" : "ham"}`;
  document.querySelector("#result-icon").innerHTML = isSpam
    ? '<svg viewBox="0 0 24 24"><path d="M12 2 2 20h20L12 2Zm1 14h-2v-2h2v2Zm0-4h-2V8h2v4Z"/></svg>'
    : '<svg viewBox="0 0 24 24"><path d="m9 16.2-3.5-3.5L4.1 14.1 9 19 20.3 7.7l-1.4-1.4L9 16.2Z"/></svg>';
  document.querySelector("#result-label").textContent = data.display_label;
  document.querySelector("#confidence").textContent = `${data.confidence.toFixed(2)}% confidence`;
  document.querySelector("#spam-value").textContent = `${data.spam_probability.toFixed(2)}%`;
  document.querySelector("#spam-meter").style.width = `${data.spam_probability}%`;
  document.querySelector("#result-guidance").textContent = isSpam
    ? "This message contains patterns commonly associated with spam. Avoid clicking links or sharing personal information."
    : "This message appears legitimate. Stay cautious when a sender asks for passwords, payments, or sensitive information.";
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  errorBox.textContent = "";
  errorBox.classList.remove("visible");
  result.classList.remove("visible");
  submitButton.classList.add("loading");
  submitButton.disabled = true;

  try {
    if (!messageInput.value.trim()) throw new Error("Please enter a message to analyze.");
    await modelReady;
    showResult(classifyMessage(messageInput.value));
  } catch (error) {
    errorBox.textContent = error.message;
    errorBox.classList.add("visible");
  } finally {
    submitButton.classList.remove("loading");
    submitButton.disabled = false;
  }
});
