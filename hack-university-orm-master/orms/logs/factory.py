# flake8: noqa
"""Factory to create Log, Ship, and User instances."""

from logs.models import Ship, Log
from django.contrib.auth.models import User
import random


def create_user(**extra_fields):
    """Create a django User."""
    username = random.choice(HUMAN_NAMES)
    first_name, last_name = username.split(' ')
    email = '{}@usstartfleet'.format(first_name.lower())
    created = False
    retry = 3
    defaults = {
        'username': username,
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
    }
    defaults.update(extra_fields)
    while not created and retry:
        user, created = User.objects.get_or_create(**defaults)
        retry -= 1

    return user


def create_ship():
    """Create a Ship."""
    ship, created = Ship.objects.get_or_create(name=random.choice(SHIP_NAMES))
    if created:
        ship.capacity = random.randrange(300, 3000, 10)
        ship.save()
    return ship


def create_log():
    """Create a random Log."""
    message, author = random.choice(MESSAGES)
    title = 'As {} once said'.format(author)
    captains_log = random.triangular(1, 10) < 5
    ship = Ship.objects.all().order_by('?').first()
    user = ship.passengers.all().order_by('?').first()
    log = Log.objects.create(
        user=user,
        title=title,
        message=message,
        captains_log=captains_log,
        ship=ship,
    )
    return log


def assign_users_to_ships():
    """Assign each user to a ship"""
    for user in User.objects.all():
        ship = create_ship()
        ship.passengers.add(user)


HUMAN_NAMES = [
    'Teisha Belmont',
    'Britteny Centrich',
    'Victorina Macbeth',
    'Ardelia Smith',
    'Phoebe Tindal',
    'Neomi Diseth',
    'Evelynn Dewitt',
    'Makeda Phillips',
    'Maddie Wakeman',
    'Allyn Bechtel',
    'Lorilee McLaren',
    'Maddie McLaren',
    'Lindsy Ducote',
    'Merissa Linkovich',
    'Natalya Alder',
    'Victorina Gammon',
    'Veronika Irani',
    'Katherina Bowdoin',
    'Walton Foxwell',
    'Raphael Vanlaere',
    'Isaias Leath',
    'Darwin Calder',
    'Stefan Wynn',
    'Chet Vilchis',
    'Raphael Buccheri',
    'Rory Barick',
    'Galen Corwin',
    'Malik Corwin',
    'Walton Foxwell',
    'Lucius Kinton',
    'Alden Paulsen',
    'Lenard Volante',
    'Benedict Kehoe',
    'Dante Kehoe',
    'Merlin Dowe',
    'Scotty Paulsen',
    'Willian Sarratt',
    'Jacinto Cantos',
]

SHIP_NAMES = [
    "USS Voyager",
    "USS Orion",
    "USS Ares",
    "USS Luna",
]


MESSAGES = [
    ['"The gem cannot be polished without friction, nor man perfected without trials."',
  ' Chinese proverb '],
 ['"An investment in knowledge always pays the best interest."',
  '  Benjamin Franklin'],
 ['Remember, you can earn more money, but time when spent is gone forever.',
  'Zig Ziglar '],
 ['"The greatest of all weaknesses is the fear of appearing weak."',
  ' J. B. Bossuet, Politics from Holy Writ, 1709'],
 ['"The first requisite of success is the ability to apply your physical and mental energies to one problem without growing weary."',
  ' Thomas Edison '],
 ['"We don\'t stop playing because we grow old; we grow old because we stop playing." ',
  ' George Bernard Shaw'],
 ['"Great things are not done by impulse, but by a series of small things brought together." ',
  'Vincent Van Gogh'],
 ['"I feel that the greatest reward for doing is the opportunity to do more." ',
  'Jonas Salk '],
 ["You've got to be before you can do, and do before you can have.",
  'Zig Ziglar '],
 ['A superior man is modest in his speech, but exceeds in his actions.',
  ' Confucius'],
 ['Ability will never catch up with the demand for it. ', 'Confucius '],
 ['No matter how busy you may think you are, you must find time for reading, or surrender yourself to self-chosen ignorance.',
  ' Confucius'],
 ['Our greatest glory is not in never falling, but in rising every time we fall.',
  ' Confucius'],
 ["Real knowledge is to know the extent of one's ignorance.", ' Confucius'],
 ['Learning without thought is labor lost; thought without learning is perilous.',
  'Confucius '],
 ['"The only worthwhile achievements of man are those which are socially useful."',
  'Alfred Adler '],
 ['"God put me on Earth to accomplish a certain number of things. Right now I\'m so far behind I will never die! " ',
  'Anonymous '],
 ['Lack of direction, not lack of time, is the problem. We all have twenty-four hour days. ',
  'Zig Ziglar'],
 ['"Destiny is not a matter of chance, it is a matter of choice; it is not a thing to be waited for, it is a thing to be achieved." ',
  'William Jennings Bryan '],
 ['"Unless a man undertakes more than he possibly can do, he will never do all that he can." ',
  'Henry Drummond '],
 ['"The best job goes to the person who can get it done without passing the buck or coming back with excuses." ',
  'Napolean Hill'],
 ['"Only those who dare to fail greatly can ever achieve greatly." ',
  ' Robert Francis Kennedy '],
 ['"It is time for us all to stand and cheer for the doer, the achiever \xe2\x80\x94 the one who recognizes the challenge and does something about it. " ',
  'Vince Lombardi'],
 ['"The heights by great men reached and kept; Were not obtained by sudden flight; But they, while their companions slept; Were toiling upward in the night."',
  'Henry Wadsworth Longfellow'],
 ['"You don\'t drown by falling in water; you only drown if you stay there."',
  'Zig Ziglar '],
 ['"What you get by achieving your goals is not as important as what you become by achieving your goals."',
  'Zig Ziglar'],
 ['"Obstacles are things a person sees when he takes his eyes off his goal."',
  'E. Joseph Crossman '],
 ['"The man who can drive himself further once the effort gets painful is the man who will win."',
  'Roger Bannister '],
 ['"You\'ll never achieve your dreams if they don\'t become goals."',
  'Anonymous '],
 ['"The spirit, the will to win, and the will to excel are the things that endure. These qualities are so much more important than the events that occur." ',
  'Vince Lombardi'],
 ['"Lombardi time" is the principle that one should arrive 10-15 minutes early, or else be considered late.',
  'Vince Lombardi'],
 ['"Every worthwhile accomplishment, big or little, has its stages of drudgery and triumph; a beginning, a struggle and a victory." ',
  'Ghandi '],
 ['"The price of success is hard work, dedication to the job at hand, and the determination that whether we win or lose, we have applied the best of ourselves to the task at hand."',
  'Vince Lombardi'],
 ['"A failure establishes only this, that our determination to succeed was not strong enough."',
  'Christian Nestell Bove '],
 ['"He who has a why to live for can bear almost any how." ',
  ' Friedrich Nietzsche'],
 ['"A leader, once convinced that a particular course of action is the right one, must....be undaunted when the going gets tough."  ',
  ' Ronald Reagan'],
 ['"\xe2\x80\x9cIt is our attitude at the beginning of a difficult task which, more than anything else, will affect it\'s successful outcome.',
  'William James '],
 ["I'ts not what happens to you that determines how far you will go in life ;it is how you handle what happens to you.",
  'Zig Ziglar'],
 ['"Holding on to anger is like grasping a hot coal with the intent of throwing it at someone else; you are the one who gets burned."',
  ' Buddha'],
 ['"The optimist sees opportunity in every danger; the pessimist sees danger in every opportunity." ',
  'Winston Churchill '],
 ['"A positive attitude may not solve all your problems, but it will annoy enough people to make it worth the effort."',
  'Herm Albright '],
 ['"There are no menial jobs, only menial attitudes." ',
  'William John Bennett '],
 ['hard work beats talent when talent doesn\'t work hard ', 'tom notke'],
 ["if you do what you've always done, you'll get what you've always got ",
  '? '],
 ['"You can tell what a man is by what he does when he hasn\'t anything to do."',
  'Anonymous '],
 ['"What lies behind us and what lies before us are tiny matters compared to what lies within us."',
  'Ralph Waldo Emerson '],
 ['"On the mountains of truth you can never climb in vain: either you will reach a point higher up today, or you will be training your powers so that you will be able to climb higher tomorrow."',
  'Friedrich Nietzsche '],
 ['"People of mediocre ability sometimes achieve outstanding success because they don\'t know when to quit. Most men succeed because they are determined to." ',
  'George E. Allen '],
 ['"Success seems to be connected with action. Successful men keep moving. They make mistakes, but they don\'t quit." ',
  'Conrad Hilton '],
 ['"Good ideas are not adopted automatically. They must be driven into practice with courageous patience." ',
  'Admiral Hyman Rickover '],
 ['"In order to get from what was to what will be, you must go through what is." ',
  'Anonymous '],
 ['"Perseverance is not a long race; it is many short races one after another." ',
  'Walter Elliott '],
 ['"Victory is always possible for the person who refuses to stop fighting." ',
  'Napoleon Hill '],
 ['"Learning is not compulsory. . . neither is survival." ',
  'Dr. W. Edwards Deming '],
 ['"What we think or what we believe is, in the end, of little consequence. The only thing of consequence is what we do." ',
  ' John Ruskin'],
 ['"Have no fear of perfection - you\'ll never reach it." ', 'Salvidor Dali'],
 ['"The important thing is this: to be able, at any moment, to sacrifice what we are for what we could become." ',
  'Maharishi Mahesh Yogi'],
 ['"Undoubtedly a man is to labor to better his condition, but first to better himself" ',
  'William Ellery Channing'],
 ['"Getting what you want is not nearly as important as giving what you have." ',
  'Tom Krause'],
 ['"To gain that which is worth having, it may be necessary to lose everything else." ',
  'Bernadette Devlin'],
 ['"Sweat plus sacrifice equals success." ', 'Charlie Finley'],
 ['"One-half of knowing what you want is knowing what you must give up before you get it." ',
  'Sidney Howard'],
 ['"Dreams do come true, if we only wish hard enough, You can have anything in life if you will sacrifice everything else for it." ',
  'James Matthew Barrie'],
 ['"Artists must be sacrificed to their art. Like bees, they must put their lives into the sting they give." ',
  'Ralph Waldo Emerson'],
 ['"Success is often the result of taking a misstep in the right direction." ',
  'Al Bernstein'],
 ['"A successful man is one who can lay a firm foundation with the bricks others have thrown at him." ',
  'David Brinkley'],
 ['"Are you bored with life? Then throw yourself into some work you believe in with all your heart, live for it, die for it, and you will find happiness that you had thought could never be yours." ',
  'Dale Carnegie'],
 ['"Instead of worrying about what people say of you, why not spend time trying to accomplish something they will admire." ',
  'Dale Carnegie'],
 ['"The successful man will profit from his mistakes and try again in a different way." ',
  'Dale Carnegie'],
 ['"Inaction breeds doubt and fear. Action breeds confidence and courage. If you want to conquer fear, do not sit home and think about it. Go out and get busy." ',
  'Dale Carnegie'],
 ['"Success means getting up one more time than you fall." ',
  ' Oliver Goldsmith'],
 ['"Never stop." ', ' Greg Bigwood'],
 ['"Living well is the best revenge." ', ' George Herbert'],
 ['"Think like a man of action, act like a man of thought." ',
  ' Henry Bergson'],
 ['"The difference between what we do and what we are capable of doing would suffice to solve most of the world\'s problem." ',
  ' Gandhi'],
 ['"An ounce of practice is worth more than tons of preaching." ', ' Gandhi'],
 ['"First they ignore you, then they laugh at you, then they fight you, then you win." ',
  ' Gandhi'],
 [' "I look only to the good qualities of men. Not being faultless myself, I won\'t presume to probe into the faults of others." ',
  ' Gandhi'],
 [' "Man becomes great exactly in the degree in which he works for the welfare of his fellow-men." ',
  ' Gandhi'],
 [' "I suppose leadership at one time meant muscles; but today it means getting along with people." ',
  ' Gandhi'],
 [' "Constant development is the law of life, and a man who always tries to maintain his dogmas in order to appear consistent drives himself into a false position." ',
  ' Gandhi'],
]
