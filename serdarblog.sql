-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Anamakine: 127.0.0.1
-- Üretim Zamanı: 01 Mar 2023, 18:55:54
-- Sunucu sürümü: 10.4.27-MariaDB
-- PHP Sürümü: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Veritabanı: `serdarblog`
--

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `articles`
--

CREATE TABLE `articles` (
  `id` int(11) NOT NULL,
  `title` text NOT NULL,
  `author` text NOT NULL,
  `content` text NOT NULL,
  `created_date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Tablo döküm verisi `articles`
--

INSERT INTO `articles` (`id`, `title`, `author`, `content`, `created_date`) VALUES
(7, 'Code makalesi nasıl yayınlanır ? ', 'serdardyck', '<p><em><strong>Merhabalar eğer code yayınlamak istiyorsanız şu adımları uygulayın;</strong></em></p>\r\n\r\n<ol>\r\n	<li><b><i>ilk olark bir hesaba ihtiyacınız var &uuml;ste bulunan <a href=\"http://127.0.0.1:5000/register\">kayıt ol</a> tuşunabasarak kayıt olun</i></b></li>\r\n	<li><b><i>Giriş Yapın giriş yapmazsanız hi&ccedil; bir şekilde işlem yapamazsınız.</i></b></li>\r\n	<li><b><i>Kontrol Paneline girip bir makale oluşturun</i></b></li>\r\n	<li><b><i><img alt=\"\" src=\"file:///C:/Users/serda/OneDrive/Masa%C3%BCst%C3%BC/s1.png\" />Makale oluştur sayfasında makale i&ccedil;eriği&#39;nin &uuml;st&uuml;nde bulunan ara&ccedil;lardan Kaynak a basın</i></b></li>\r\n	<li><b><i>&ouml;n&uuml;n&uuml;ze gelen sayfada aşağıda bulunan &lt;pre class=&quot;prettyprint&quot;&gt;...&lt;/pre&gt; tagları i&ccedil;erisinde kodunuzu yapıştırın.&nbsp;</i></b></li>\r\n	<li><b><i>Ve bitti makaleniz aşağıdaki gibi g&ouml;z&uuml;kecektir</i></b></li>\r\n	<li>\r\n	<pre class=\"prettyprint\">\r\nprint(&quot;hello world&quot;)</pre>\r\n	</li>\r\n</ol>\r\n', '2023-03-01 13:54:23');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `contact`
--

CREATE TABLE `contact` (
  `name` text NOT NULL,
  `username` text NOT NULL,
  `mesaj` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Tablo döküm verisi `contact`
--

INSERT INTO `contact` (`name`, `username`, `mesaj`) VALUES
('serdar', 'dayıcık', 'merhaba cok kötü site'),
('serdar dayıcık', 'serdardyck', 'merhaba cok kötü site'),
('eqweqwe', '1234', 'merhaba cok kötü site');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` text NOT NULL,
  `email` text NOT NULL,
  `username` text NOT NULL,
  `password` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Tablo döküm verisi `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `username`, `password`) VALUES
(13, 'serdar dayıcık', 'serdardayicik123@gmail.com', 'serdardyck', '$5$rounds=535000$GJ3gOMSvxDGWRLy8$V5wpXrqoEjx8JcQcZSIlpkdeZfowH8p2otvUieCc4N3'),
(14, 'weqeq', 'serdar@gmail.com', 'serdar', '$5$rounds=535000$GUsagzEWfDpfKSU6$BBx6UauXy/gdxmpS2C5JbFFubf8faDCOTFB3hgxpTFA');

--
-- Dökümü yapılmış tablolar için indeksler
--

--
-- Tablo için indeksler `articles`
--
ALTER TABLE `articles`
  ADD PRIMARY KEY (`id`);

--
-- Tablo için indeksler `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- Dökümü yapılmış tablolar için AUTO_INCREMENT değeri
--

--
-- Tablo için AUTO_INCREMENT değeri `articles`
--
ALTER TABLE `articles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- Tablo için AUTO_INCREMENT değeri `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
