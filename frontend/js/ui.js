document.addEventListener("DOMContentLoaded", async () => {
  const api = new ConsciousCommuteAPI();
  const graph = new RailwayClientGraph();
  
  window.railwayGraph = graph; // Make globally accessible for map.js

  const selectSource = document.getElementById("select-source");
  const selectDestination = document.getElementById("select-destination");
  const selectSubject = document.getElementById("select-subject");
  const selectModule = document.getElementById("select-module");
  const moduleGroup = document.getElementById("module-group");
  const togglePeak = document.getElementById("toggle-peak");
  const btnSubmit = document.getElementById("btn-submit");
  const metricDuration = document.getElementById("metric-duration");
  const metricStations = document.getElementById("metric-stations");
  const studyPanel = document.getElementById("study-panel");
  const lineButtons = document.querySelectorAll(".line-btn");

  let selectedSource = "";
  let selectedDestination = "";
  let selectedLine = "";

  // 1. Initialize Railway Data & Map
  const success = await graph.initialize();
  if (success) {
    initMap(graph);
    populateStations();
  }

  // 2. Fetch Available Syllabi
  const syllabi = await api.fetchSyllabi();
  populateSubjects(syllabi);

  // 3. Populate Select Options
  function populateStations() {
    // Filter stations by line if a specific line is selected
    const stations = selectedLine 
      ? graph.getStationsForLine(selectedLine).sort()
      : graph.getStations();
      
    const currentSource = selectSource.value;
    const currentDest = selectDestination.value;
    
    selectSource.innerHTML = '<option value="">-- Choose Source --</option>';
    selectDestination.innerHTML = '<option value="">-- Choose Destination --</option>';

    stations.forEach(station => {
      const opt1 = document.createElement("option");
      opt1.value = station;
      opt1.textContent = station;
      if (station === currentSource) opt1.selected = true;
      selectSource.appendChild(opt1);

      const opt2 = document.createElement("option");
      opt2.value = station;
      opt2.textContent = station;
      if (station === currentDest) opt2.selected = true;
      selectDestination.appendChild(opt2);
    });
  }

  function populateSubjects(subjectsList) {
    selectSubject.innerHTML = '<option value="">-- Choose Subject --</option>';
    subjectsList.forEach(subject => {
      const opt = document.createElement("option");
      opt.value = subject;
      opt.textContent = subject;
      selectSubject.appendChild(opt);
    });
  }

  // 4. Line Selector Panning & Filtering
  lineButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      const wasActive = btn.classList.contains("active");
      
      // Reset active class on all buttons
      lineButtons.forEach(b => b.classList.remove("active"));
      
      if (wasActive) {
        // Toggle selection off
        selectedLine = "";
      } else {
        // Toggle selection on
        btn.classList.add("active");
        selectedLine = btn.getAttribute("data-line");
        focusMapOnLine(selectedLine);
      }
      
      // Update dropdowns based on the selected line filter
      populateStations();
      
      // Clean up invalid selections that do not exist on the newly filtered line
      if (selectedLine) {
        const lineStations = graph.getStationsForLine(selectedLine);
        if (selectSource.value && !lineStations.includes(selectSource.value)) {
          selectSource.value = "";
        }
        if (selectDestination.value && !lineStations.includes(selectDestination.value)) {
          selectDestination.value = "";
        }
      }
      updateRoute();
    });
  });

  function focusMapOnLine(lineName) {
    const lineCoords = {
      'Western': [19.1197, 72.8464], // Andheri
      'Central': [19.0864, 72.9081], // Ghatkopar
      'Harbour': [19.0340, 73.0190]  // Nerul
    };
    if (map && lineCoords[lineName]) {
      map.setView(lineCoords[lineName], 11.5);
    }
  }

  // 5. Update Selection and Route Summary
  function updateRoute() {
    selectedSource = selectSource.value;
    selectedDestination = selectDestination.value;

    if (!selectedSource || !selectedDestination) {
      metricDuration.textContent = "0 min";
      metricStations.textContent = "0";
      btnSubmit.disabled = true;
      updateMapMarkers(selectedSource, selectedDestination, null);
      return;
    }

    const isPeak = togglePeak.checked;
    const { duration, path } = graph.calculateTravelTime(selectedSource, selectedDestination, isPeak);

    if (duration !== null) {
      metricDuration.textContent = `${duration} min`;
      metricStations.textContent = path.length;
      btnSubmit.disabled = !selectSubject.value; // Enable if subject is also selected
      updateMapMarkers(selectedSource, selectedDestination, path);
    } else {
      metricDuration.textContent = "N/A";
      metricStations.textContent = "0";
      btnSubmit.disabled = true;
      updateMapMarkers(selectedSource, selectedDestination, null);
    }
  }

  selectSource.addEventListener("change", updateRoute);
  selectDestination.addEventListener("change", updateRoute);
  togglePeak.addEventListener("change", updateRoute);

  selectSubject.addEventListener("change", async () => {
    updateRoute();
    const subject = selectSubject.value;
    
    if (!subject) {
      moduleGroup.style.display = "none";
      return;
    }
    
    // Clear previous options except "any module"
    selectModule.innerHTML = '<option value="any module">Any Module</option>';
    
    try {
      selectModule.disabled = true;
      const optionLoading = document.createElement("option");
      optionLoading.text = "Loading modules...";
      selectModule.appendChild(optionLoading);
      moduleGroup.style.display = "block";
      
      const modules = await api.getModules(subject);
      
      if (selectModule.contains(optionLoading)) {
        selectModule.removeChild(optionLoading);
      }
      selectModule.disabled = false;
      
      modules.forEach(mod => {
        const opt = document.createElement("option");
        opt.value = mod;
        opt.textContent = mod;
        selectModule.appendChild(opt);
      });
    } catch (e) {
      console.error("Failed to load modules:", e);
      selectModule.disabled = false;
    }
  });

  // 6. Map Station Selection Bridge
  window.onMapStationSelect = (stationName) => {
    if (!selectSource.value) {
      selectSource.value = stationName;
    } else if (!selectDestination.value) {
      selectDestination.value = stationName;
    } else {
      // Clear destination and change source
      selectSource.value = stationName;
      selectDestination.value = "";
    }
    updateRoute();
  };

  btnSubmit.addEventListener("click", async () => {
    const source = selectSource.value;
    const destination = selectDestination.value;
    const subject = selectSubject.value;
    const module = selectModule.value || "any module";
    const isPeak = togglePeak.checked;

    if (!source || !destination || !subject) return;

    // Transition main container to study view on mobile
    const mainContainer = document.querySelector(".main-container");
    mainContainer.classList.add("mobile-study-active");

    // Show Loader State
    studyPanel.innerHTML = `
      <div class="loader-container" style="position: relative; width: 100%; height: 100%;">
        <button class="btn-nav mobile-only-btn" id="btn-mobile-loader-back" style="position: absolute; top: 0; left: 0; padding: 0.4rem 0.8rem; font-size: 0.75rem; z-index: 10; display: flex; align-items: center; gap: 0.25rem;">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>
          Back
        </button>
        <div class="spinner"></div>
        <div class="loader-text">AI Orchestrator invoking Syllabus Agent...</div>
      </div>
    `;

    const loaderBackBtn = document.getElementById("btn-mobile-loader-back");
    if (loaderBackBtn) {
      loaderBackBtn.addEventListener("click", () => {
        mainContainer.classList.remove("mobile-study-active");
      });
    }

    // Dynamic loader texts to simulate agent progress
    const loaderTexts = [
      "Syllabus Agent reading PDF syllabus...",
      "Extracting modules and topics...",
      "Invoking Content Generator Agent...",
      "Formatting micro-study plan for phone screen...",
      "Wrapping up study materials..."
    ];
    let loaderIdx = 0;
    const loaderInterval = setInterval(() => {
      const loaderTextEl = document.querySelector(".loader-text");
      if (loaderTextEl && loaderIdx < loaderTexts.length) {
        loaderTextEl.textContent = loaderTexts[loaderIdx++];
      }
    }, 2500);

    try {
      const result = await api.generateStudyPlan(source, destination, subject, isPeak, module);
      clearInterval(loaderInterval);

      if (result.is_too_short) {
        renderGuardrail(result.message);
      } else {
        renderStudyPlan(result);
      }
    } catch (e) {
      clearInterval(loaderInterval);
      studyPanel.innerHTML = `
        <div class="guardrail-alert" style="background: rgba(239, 68, 68, 0.1); border-color: #ef4444; color: #fca5a5; position: relative; padding: 2.5rem 1rem 1rem 1rem;">
          <button class="btn-nav mobile-only-btn" id="btn-mobile-error-back" style="position: absolute; top: 0.5rem; left: 0.5rem; padding: 0.3rem 0.6rem; font-size: 0.7rem; z-index: 10; display: flex; align-items: center; gap: 0.25rem;">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>
            Back
          </button>
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 0.5rem; flex-shrink: 0;"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
          <div>
            <strong>Error Generating Plan:</strong>
            <p id="error-message-text" style="font-size: 0.85rem; margin-top: 0.25rem;"></p>
          </div>
        </div>
      `;
      document.getElementById("error-message-text").textContent = e.message || "An unexpected error occurred. Please ensure your GEMINI_API_KEY is set in your .env file.";
      const errBackBtn = document.getElementById("btn-mobile-error-back");
      if (errBackBtn) {
        errBackBtn.addEventListener("click", () => {
          mainContainer.classList.remove("mobile-study-active");
        });
      }
    }
  });

  function renderGuardrail(message) {
    studyPanel.innerHTML = `
      <div class="guardrail-alert" style="position: relative; padding: 2.5rem 1rem 1rem 1rem;">
        <button class="btn-nav mobile-only-btn" id="btn-mobile-guard-back" style="position: absolute; top: 0.5rem; left: 0.5rem; padding: 0.3rem 0.6rem; font-size: 0.7rem; z-index: 10; display: flex; align-items: center; gap: 0.25rem;">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>
          Back
        </button>
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 0.5rem; flex-shrink: 0;"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
        <div>
          <strong>Commute Too Short:</strong>
          <p id="guardrail-message-text" style="font-size: 0.85rem; margin-top: 0.25rem;"></p>
        </div>
      </div>
    `;
    document.getElementById("guardrail-message-text").textContent = message;
    const guardBackBtn = document.getElementById("btn-mobile-guard-back");
    if (guardBackBtn) {
      guardBackBtn.addEventListener("click", () => {
        document.querySelector(".main-container").classList.remove("mobile-study-active");
      });
    }
  }

  function renderStudyPlan(result) {
    // Split the study plan into individual cards using the "---" separator.
    // We clean up empty cards or whitespace.
    const rawCards = result.study_plan.split(/\n---+\r?\n/);
    const cards = rawCards
      .map(card => card.trim())
      .filter(card => card.length > 0);

    if (cards.length === 0) {
      // Fallback if no split dividers are found
      cards.push(result.study_plan);
    }

    let currentCardIndex = 0;

    // Render basic carousel scaffolding with Focus Toggles & Mobile Back Toggles
    studyPanel.innerHTML = `
      <div class="study-card-deck">
        <div style="display: flex; gap: 0.5rem; margin-bottom: 0.5rem; justify-content: space-between; align-items: center;">
          <button class="btn-nav mobile-only-btn" id="btn-mobile-back" style="padding: 0.4rem 0.8rem; font-size: 0.75rem; display: flex; align-items: center; gap: 0.25rem;">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>
            Back to Route
          </button>
          <button class="btn-nav laptop-only-btn" id="btn-laptop-focus" style="margin-left: auto;">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 0.25rem;"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/><line x1="11" y1="8" x2="11" y2="14"/><line x1="8" y1="11" x2="14" y2="11"/></svg>
            Zoom In (Focus)
          </button>
        </div>

        <!-- Session Progress Section (Placed ABOVE cards) -->
        <div style="display: flex; flex-direction: column; gap: 0.4rem; margin-bottom: 0.75rem; background: rgba(20, 22, 33, 0.25); border: 1px solid var(--border-glass); padding: 0.6rem 0.8rem; border-radius: 10px;">
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 0.75rem; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.5px; font-weight: 600;">Study Progress</span>
            <span class="page-indicator" id="card-page-indicator" style="font-size: 0.8rem; font-weight: 700; color: var(--text-primary);">Card 1 of ${cards.length}</span>
          </div>
          <div class="progress-bar-container" style="margin-top: 0.1rem;">
            <div class="progress-bar-fill" id="carousel-progress-fill"></div>
          </div>
        </div>

        <!-- Study Card Deck Container -->
        <div class="study-card-container" id="cards-container">
          <!-- Card elements populated dynamically -->
        </div>

        <!-- Navigation Row (Placed BELOW cards) -->
        <div class="carousel-controls-bottom" style="display: flex; justify-content: space-between; align-items: center; margin-top: 0.75rem; background: rgba(20, 22, 33, 0.25); border: 1px solid var(--border-glass); padding: 0.6rem 0.8rem; border-radius: 10px; gap: 1rem;">
          <button class="btn-nav" id="btn-card-prev" disabled style="flex: 1; display: flex; align-items: center; justify-content: center; gap: 0.25rem; padding: 0.5rem 1rem;">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>
            Previous
          </button>
          <button class="btn-nav" id="btn-card-next" style="flex: 1; display: flex; align-items: center; justify-content: center; gap: 0.25rem; padding: 0.5rem 1rem;">
            Next
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
          </button>
        </div>
      </div>
    `;

    const container = document.getElementById("cards-container");
    const prevBtn = document.getElementById("btn-card-prev");
    const nextBtn = document.getElementById("btn-card-next");
    const indicator = document.getElementById("card-page-indicator");
    const progressFill = document.getElementById("carousel-progress-fill");

    // Pre-parse all cards from Markdown to HTML
    const cardElements = cards.map((cardText, idx) => {
      const cardDiv = document.createElement("div");
      cardDiv.className = "study-card";
      if (idx === 0) cardDiv.classList.add("active");
      cardDiv.innerHTML = DOMPurify.sanitize(marked.parse(cardText));
      container.appendChild(cardDiv);
      return cardDiv;
    });

    function showCard(index) {
      cardElements.forEach((el, idx) => {
        el.classList.toggle("active", idx === index);
      });

      // Update Nav Buttons
      prevBtn.disabled = index === 0;
      nextBtn.disabled = index === cards.length - 1;

      // Update Page Indicator text & Progress bar fill
      indicator.textContent = `Card ${index + 1} of ${cards.length}`;
      const percentage = ((index + 1) / cards.length) * 100;
      progressFill.style.width = `${percentage}%`;
    }

    // Set initial progress
    progressFill.style.width = `${(1 / cards.length) * 100}%`;

    // Add click event listeners
    prevBtn.addEventListener("click", () => {
      if (currentCardIndex > 0) {
        currentCardIndex--;
        showCard(currentCardIndex);
      }
    });

    nextBtn.addEventListener("click", () => {
      if (currentCardIndex < cards.length - 1) {
        currentCardIndex++;
        showCard(currentCardIndex);
      }
    });

    // Mobile Back Button
    const mobileBackBtn = document.getElementById("btn-mobile-back");
    if (mobileBackBtn) {
      mobileBackBtn.addEventListener("click", () => {
        const mainContainer = document.querySelector(".main-container");
        mainContainer.classList.remove("mobile-study-active");
      });
    }

    // Laptop Focus Mode Toggle
    const laptopFocusBtn = document.getElementById("btn-laptop-focus");
    if (laptopFocusBtn) {
      laptopFocusBtn.addEventListener("click", () => {
        const mainContainer = document.querySelector(".main-container");
        const isFocus = mainContainer.classList.toggle("focus-active");
        if (isFocus) {
          laptopFocusBtn.innerHTML = `
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 0.25rem;"><path d="M4 14h6v6"/><path d="M20 10h-6V4"/><path d="M14 10l7-7"/><path d="M10 14l-7 7"/></svg>
            Exit Focus
          `;
        } else {
          laptopFocusBtn.innerHTML = `
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 0.25rem;"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/><line x1="11" y1="8" x2="11" y2="14"/><line x1="8" y1="11" x2="14" y2="11"/></svg>
            Zoom In (Focus)
          `;
        }
        if (window.map) {
          setTimeout(() => { window.map.invalidateSize(); }, 300);
        }
      });
    }

    // Support Keyboard Left/Right arrow keys for laptops (with cleanup)
    const keyboardHandler = (e) => {
      if (e.key === "ArrowLeft" && currentCardIndex > 0) {
        currentCardIndex--;
        showCard(currentCardIndex);
      } else if (e.key === "ArrowRight" && currentCardIndex < cards.length - 1) {
        currentCardIndex++;
        showCard(currentCardIndex);
      }
    };
    
    if (window.currentKeyboardHandler) {
      document.removeEventListener("keydown", window.currentKeyboardHandler);
    }
    window.currentKeyboardHandler = keyboardHandler;
    document.addEventListener("keydown", keyboardHandler);

    // Support touch swiping for phone users
    let startX = 0;
    container.addEventListener("touchstart", (e) => {
      startX = e.touches[0].clientX;
    }, { passive: true });

    container.addEventListener("touchend", (e) => {
      const endX = e.changedTouches[0].clientX;
      const diffX = startX - endX;
      // Threshold 50px
      if (diffX > 50 && currentCardIndex < cards.length - 1) {
        currentCardIndex++;
        showCard(currentCardIndex);
      } else if (diffX < -50 && currentCardIndex > 0) {
        currentCardIndex--;
        showCard(currentCardIndex);
      }
    }, { passive: true });

    // Auto-activate Focus Mode by default on laptops
    if (window.innerWidth > 768) {
      const mainContainer = document.querySelector(".main-container");
      mainContainer.classList.add("focus-active");
      if (laptopFocusBtn) {
        laptopFocusBtn.innerHTML = `
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 0.25rem;"><path d="M4 14h6v6"/><path d="M20 10h-6V4"/><path d="M14 10l7-7"/><path d="M10 14l-7 7"/></svg>
          Exit Focus
        `;
      }
      if (window.map) {
        setTimeout(() => { window.map.invalidateSize(); }, 300);
      }
    }

    // Auto-render LaTeX Math expressions
    if (window.renderMathInElement) {
      window.renderMathInElement(studyPanel, {
        delimiters: [
          {left: '$$', right: '$$', display: true},
          {left: '$', right: '$', display: false},
          {left: '\\(', right: '\\)', display: false},
          {left: '\\[', right: '\\[', display: true}
        ],
        throwOnError: false
      });
    }
  }
});
