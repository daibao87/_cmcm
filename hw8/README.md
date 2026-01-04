夏農信道編碼定理 (Shannon's Channel Coding Theorem)這是資訊理論中最著名的定理之一，它告訴我們通訊的極限在哪裡。
核心概念： 每個通訊信道都有一個特定的容量（Capacity, $C$）。
定理內容： 如果你的資訊傳輸速率 $R$ 小於信道容量 $C$ ($R < C$)，那麼理論上一定存在一種編碼方式，使得接收端的錯誤率可以趨近於零。
反之： 如果 $R > C$，則錯誤率不可能任意小，一定會發生資訊丟失。
意義： 這證明了我們可以透過增加編碼的複雜度（加入冗餘位元，如上面的漢明碼），在有雜訊的信道中實現幾乎完美的通訊，只要我們不超過速度極限。
2. 夏農-哈特利定理 (Shannon–Hartley Theorem)這是一個具體的公式，用來計算在高斯白雜訊（AWGN）環境下，信道的理論容量是多少。
公式：$$C = B \log_2(1 + \frac{S}{N})$$$C$ (Channel Capacity)： 信道容量（單位：bits per second, bps）。
$B$ (Bandwidth)： 信道頻寬（單位：Hz）。$S/N$ (Signal-to-Noise Ratio, SNR)： 信噪比（訊號功率 $S$ 除以雜訊功率 $N$）。
ai對話:https://chatgpt.com/share/695a559a-ad50-8009-a502-c1e002ed333f
