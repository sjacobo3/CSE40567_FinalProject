'''Imports'''
import os, time, random, string
import matplotlib.pyplot as plt
import Vigenere, TripleDES as TripDES, RSA, AES

'''Define Global Variables and Set Up Keys'''
INPUT_SIZES = [10, 50, 100, 300, 550, 775, 1000, 2000, 3000, 5500, 7750]
N_REPEATS = 3
EVALUATION_TIMES = {
    "Vigenere": {'encryption_times': [], 'decryption_times': [], 'color': '#e69138ff', 'marker': 's'},
    "3DES": {'encryption_times': [], 'decryption_times': [], 'color': '#9cbb59ff', 'marker': '^'},
    "RSA": {'encryption_times': [], 'decryption_times': [], 'color': '#c0504dff', 'marker':'D'},
    "AES": {'encryption_times': [], 'decryption_times': [], 'color':'#4bacc6ff', 'marker':'o'}
}

# vigenere key
VIG_KEY = "abcdefghijk"

# 3DES key
K1 = "0000000011111111000000001111111100000000111111110000000011111111"
K2 = "0000000000000000000000000000000000000000000000000000000000000000"
K3 = "1111111111111111111111111111111111111111111111111111111111111111"

# RSA key (2048-bit for industry standard)
E = 65537
N = 10592400571663431873594637447319596768141785848810397010576589985395475835513665357303352346264349875251609417857028392140089626497673776805238968488782022311923487969769708998370034260353863991831217402862012635035152317250950196027842306220681821987073481300136800798004833962128391994418647329324940521393320130899333994062947511616132091484212330162036272537592984034092946846392488411699725353392018077809065551304306028086905363919761315614820029946384404118077055214962219681006565305559193007076372229479100914402678623744920149908432174868528196059841996430728392015741657116917504280580906517161619443877739
D = 9623298631878364850171632943998903080274197342326011999431477551923829695016847720206889269403934509091903449175661496504464294235286850859220492588775354234619167755741920494864736101678890030633421050457102008066100128498997903805388692718397490927755956941749626261714845338344547167854504793251694212189563422605935498590214510774849782854791853283026094945574268666416147823834129940211596094020946719146335461707250868497625200912584786058413334541833911856438261398399905202441427710266121791951669956012052472713393354901696780986098905013082373537623569318586638441400844624756569880306223457346896976452993

# AES key
AES_KEY = list(os.urandom(16))

'''Define Helper Functions'''
def get_meantime_output(cipher, *args, n_repeats=N_REPEATS):
    # accumulate times for n_repeats then return the average and the output
    times = []
    for _ in range(n_repeats):
        t_start = time.perf_counter()
        output = cipher(*args)
        t_end = time.perf_counter()
        times.append(t_end - t_start)
    return sum(times) / n_repeats, output 

'''Evaluate'''
for size in INPUT_SIZES:
    # VIGENERE
    print(f'Evaluating Vigenere for {size} bytes...')
    # encryption
    vig_pt = ''.join(random.choices(string.ascii_uppercase, k=size))
    vig_enc_time, vig_ct = get_meantime_output(Vigenere.vig_encrypt, vig_pt, VIG_KEY)
    EVALUATION_TIMES['Vigenere']['encryption_times'].append(vig_enc_time)
    # decryption
    vig_dec_time, _ = get_meantime_output(Vigenere.vig_decrypt, vig_ct, VIG_KEY)
    EVALUATION_TIMES['Vigenere']['decryption_times'].append(vig_dec_time)

    # 3DES
    print(f'Evaluating 3DES for {size} bytes...')
    # encryption
    tripdes_pt = os.urandom(size)
    tripdes_enc_time, tripdes_ct = get_meantime_output(TripDES.tripdes_encrypt, tripdes_pt, K1, K2, K3)
    EVALUATION_TIMES['3DES']['encryption_times'].append(tripdes_enc_time)
    # decryption
    tripdes_dec_time, _ = get_meantime_output(TripDES.tripdes_decrypt, tripdes_ct, K1, K2, K3, True)
    EVALUATION_TIMES['3DES']['decryption_times'].append(tripdes_dec_time)

    # RSA
    print(f'Evaluating RSA for {size} bytes...')
    # encryption
    rsa_pt = os.urandom(size)
    rsa_enc_time, rsa_ct = get_meantime_output(RSA.rsa_encrypt_file, rsa_pt, E, N)
    EVALUATION_TIMES['RSA']['encryption_times'].append(rsa_enc_time)
    # decryption
    rsa_dec_time, _ = get_meantime_output(RSA.rsa_decrypt_file, rsa_ct, D, N)
    EVALUATION_TIMES['RSA']['decryption_times'].append(rsa_dec_time)

    # AES
    print(f'Evaluating AES for {size} bytes...')
    # encryption
    aes_pt = os.urandom(size)
    aes_enc_time, aes_ct = get_meantime_output(AES.aes_encrypt_file, aes_pt, AES_KEY)
    EVALUATION_TIMES['AES']['encryption_times'].append(aes_enc_time)
    # decryption
    aes_dec_time, _ = get_meantime_output(AES.aes_decrypt_file, aes_ct, AES_KEY)
    EVALUATION_TIMES['AES']['decryption_times'].append(aes_dec_time)

'''Plot Data'''
def plot(title, mode, axis):
    for cipher, data in EVALUATION_TIMES.items():
        # convert times to milliseconds
        times_ms = [t * 1000 for t in data[mode]]
        axis.plot(INPUT_SIZES, 
                  times_ms,
                  label=cipher,
                  color=data['color'],
                  marker=data['marker'],
                  linewidth=1,
                  markersize=5)
    axis.set_title(title, fontsize=12)
    axis.set_xlabel('Size of Input Data (bytes)', fontsize=10)
    axis.set_ylabel('Time (ms)', fontsize=10)
    axis.set_xscale('log')
    axis.set_xticks(INPUT_SIZES)
    axis.legend(fontsize=10)
    axis.grid(True, linestyle='--', alpha=0.4)

# plot encryption times
fig_enc, axis_enc = plt.subplots(figsize=(10,6))
plot('Encryption Efficiency', 'encryption_times', axis_enc)
plt.tight_layout()
plt.savefig('public/encryption.png', dpi=150)

# plot decryption times
fig_dec, axis_dec = plt.subplots(figsize=(10,6))
plot('Decryption Efficiency', 'decryption_times', axis_dec)
plt.tight_layout()
plt.savefig('public/decryption.png', dpi=150)