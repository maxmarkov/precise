from precise.skatervaluation.battlelatex.tables import elo_latex_table

if __name__=='__main__':
     ltx = elo_latex_table(genre='cov_likelihood',category='stocks_5_days_p25_n20')
     print(ltx)