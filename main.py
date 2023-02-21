from insta_scraper import main
from calculator import calculate_statistics
from industry_recognize import get_industries

if __name__ == '__main__':
    target_account = 'jonasroeber'
    main(target_account)
    calculate_statistics(f"profiles/{target_account}.json")
    get_industries(target_account)