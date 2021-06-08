#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 19:32:15 2020

@author: tomaszzurek
"""

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.cluster import KMeans
from sklearn.model_selection import GridSearchCV


df = pd.read_csv('train-amazon.tsv', sep='\t')

cv = CountVectorizer(min_df=5, max_df=0.5, stop_words='english')

macierz = cv.fit_transform(df['review'])

means = KMeans(n_clusters=5)
means.fit(macierz)

LDA = LatentDirichletAllocation(
    learning_method='online', random_state=42, n_components=5,  learning_decay=.7)
LDA.fit(macierz)

# gridsearch = GridSearchCV(LDA, param_grid={'n_components': [
#                           5, 10],  'learning_decay': [.5, .7]},n_jobs=-1,verbose=True)

# gridsearch.fit(macierz)
# print("Best Model's Params: ", gridsearch.best_params_)
# print("Best Log Likelihood Score: ", gridsearch.best_score_)


topic_results_lda = LDA.transform(macierz)
lda_wynik = topic_results_lda.argmax(axis=1)
print(lda_wynik)


for index, topic in enumerate(LDA.components_):
    print(f'najwazniejsz 15 slow w temacie: #{index}')
    print([cv.get_feature_names()[i] for i in topic.argsort()[-15:]])
    print('\n')
tekst = ['  Donald Trump is unabashedly praising Russian President Vladimir Putin, a day after outgoing President Obama issued tough sanctions against the country in response to alleged cyberattacks intended to influence the U. S. elections. In a tweet Friday afternoon, Trump responded to Putin’s decision not to expel U. S. diplomats from Russia in kind after Obama ordered 35 Russian diplomats to leave the country  —   admiring the Russian leader’s strategic approach over President Obama, which is the theme of Trump’s ongoing praise of Putin. Earlier Friday, Putin instead signaled he would wait to decide how to move forward until Trump takes office, giving him someone in the Oval Office who has been much friendlier and quite generous with his praise  —   a stark break from decades of U. S. foreign policy. The Russian Embassy in the U. S. also retweeted Trump’s post, which he pinned to his Twitter timeline so it would remain at the top. Trump also posted it to Instagram. On Thursday, President Obama issued a stinging rebuke to Russia after U. S. intelligence officials concluded the country had directed hacks into Democratic National Committee emails and the personal email account of Democratic nominee Hillary Clinton’s campaign chairman, John Podesta. In a statement, Obama said ”all Americans should be alarmed by Russia’s actions.” Trump’s praise of Putin stands in stark contrast not just with the outgoing administration, but with top leaders of his own party. GOP congressional leaders backed Obama’s actions on Thursday, albeit criticizing the president for being too late in taking a strong stance against Russia. House Speaker Paul Ryan called the sanctions ”overdue” but ”appropriate” and said that ”Russia does not share America’s interests.” ”The Russians are not our friends,” Senate Majority Leader Mitch McConnell said in a statement, calling the sanctions a ”good initial step.” Obama has pointed to the impact of past sanctions by the U. S. and Europe in the wake of the annexation of Crimea, maintaining that his approach has damaged Russia’s economy and isolated the country on the world stage. Trump released a brief statement Thursday evening in response to the latest actions by Obama against Russia simply stating that, ”It’s time for our country to move on to bigger and better things.” He said he would meet with U. S. intelligence officials regarding the cyberhacking, though Trump has repeatedly cast doubt on their findings and throughout the campaign dismissed reports that Russia was behind the attacks. Trump raised eyebrows throughout the campaign with his praise of Putin. ”He’s running his country, and at least he’s a leader, unlike what we have in this country,” Trump said in an interview with MSNBC in December 2015. He was pressed by host Joe Scarborough on the killings of political figures and journalists critical of Putin and deflected. That interview came just after Putin praised Trump as ”talented.” Later in the campaign, Trump suggested Russia should find emails missing from Hillary Clinton’s time as secretary of state, which his aides later said was a joke. At the time, Trump tried distancing himself from Putin. ”I never met Putin. I don’t know who Putin is. He said one nice thing about me. He said I’m a genius. I said, ’Thank you very much’ to the newspaper, and that was the end of it,” Trump said. But not long after, Trump was heavily criticized for saying Putin wasn’t going into Ukraine, even though his country had already annexed Crimea. The Republican nominee also repeated his praise of Putin as ”a leader far more than our president has been” at a national security town hall in early September. One of the most memorable clashes in Trump’s debates with Hillary Clinton was when the Democratic nominee accused him of being a ”puppet” of Russia. Trump shot back: ”No puppet. No puppet. You’re the puppet.” He often criticizes the   ”reset” with Russia that Clinton led in the early days of the Obama administration, even as Trump himself repeatedly has called for friendlier relations with Moscow. With three weeks until Inauguration Day, Trump has increasingly used his Twitter feed to weigh in on foreign policy  —   violating usual protocols where the winner of an election avoids interfering in the foreign policy actions of the sitting president. Trump’s staff has said such use of Twitter to weigh in on foreign policy won’t end once he’s in the Oval Office. So far, he’s outlined his opposition to the United States’ abstention from the U. N. Security Council vote on Israeli settlements earlier this month. Trump has also criticized China for its seizure of an unmanned U. S. Navy underwater drone, before saying the country that he’s often criticized should keep the drone. And Trump has also called for the U. S. to strengthen its nuclear arsenal and recently seemed to encourage a nuclear arms race with Russia  —   perhaps because he believes his strategic approach to Putin will work better than Obama’s.']
transformacja = cv.transform(tekst)
rezultat = LDA.transform(transformacja)
print(rezultat)
