export type Locale = "zh-CN" | "en" | "ja" | "ko" | "es" | "fr" | "de" | "pt-BR";

export type Messages = {
  app: { name: string; description: string };
  nav: {
    dashboard: string;
    opportunities: string;
    information: string;
    search: string;
  };
  lang: { label: string };
  dashboard: {
    title: string;
    subtitle: string;
    errorBackend: string;
    trendingTopics: string;
    topOpportunities: string;
    recentInformation: string;
    noOpportunities: string;
  };
  stats: {
    information: string;
    analyses: string;
    opportunities: string;
    pendingAnalysis: string;
    pendingOpportunities: string;
    sources: string;
  };
  pipeline: {
    actions: string;
    crawl: string;
    analyze: string;
    generate: string;
    completed: string;
    failed: string;
  };
  automation: {
    title: string;
    schedulerOn: string;
    schedulerOff: string;
    noJobs: string;
  };
  trends: {
    empty: string;
    avgRelevance: string;
  };
  opportunities: {
    title: string;
    subtitle: string;
    empty: string;
    loadError: string;
  };
  opportunity: {
    target: string;
    problem: string;
    nextStep: string;
  };
  information: {
    title: string;
    subtitle: string;
    empty: string;
    loadError: string;
    collected: string;
    aiInsight: string;
    relevance: string;
    awaitingAnalysis: string;
  };
  search: {
    title: string;
    subtitle: string;
    placeholder: string;
    scopeAll: string;
    scopeInformation: string;
    scopeAnalysis: string;
    scopeOpportunity: string;
    button: string;
    searching: string;
    error: string;
    results: string;
    score: string;
  };
};

export type LocaleOption = {
  value: Locale;
  nativeName: string;
};
