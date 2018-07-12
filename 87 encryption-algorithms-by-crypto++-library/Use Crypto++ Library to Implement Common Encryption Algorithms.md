---
show: step
version: 1.0
enable_checker: true
---

# C++: Use Crypto++ Library to Implement Common Encryption Algorithms

## 1. Introduction

Crypto++ library is a C++ data encryption algorithm library with open source, it supports the following algorithms: RSA, MD5, DES, AES, SHA-256 and so on. Speaking of encryption, there're symmetric encryption and asymmetric encryption. In this lab, we'll use MD5 to check the string and use AES to encrypt and decode by Crypto++ library.

#### 1.1 Learning Objectives

- Install Crypto++ library and check
- MD5 message-digest algorithm
- AES encryption algorithm

#### 1.2 Result 
![image desc](https://labex.io/upload/V/G/F/m3EeOvP3zAEC.png)

## 2. Introduce the Encryption Algorithm

According to the record, in 400 BC, the ancient Greeks invented permutation cipher. In 1881, the first phone security patent took place. During World War 2, the German army used "Enigma" cipher machine. Cryptography plays a vital role in the war.

With the development of the informational and digital society, people take the importance of information security and secrecy more and more seriously. So in 1997, the American National Standards Institute (ANSI) issued and implemented "Data Encryption Standard (DES) ". People began to fully intervene the research and application of Cryptography, with algorithms like DES, RSA, SHA and so on. As people demand more and more of the encryption strength, recently AES and ECC were invented.

You can use cryptography to do things like these: 
 Secrecy: Avoid the mark or data of the users from being read.

- Data integrity: Avoid the data from being changed.
- Authentication: Make sure the data is sent from a certain user.

#### 2.1 Introduce the Types of Encryption

Divide the the modern cryptography into two kinds by the type of secret keys:

Symmetric encryption (secret key encryption) and asymmetric encryption (public key encryption).

In symmetric encryption system, we use the same secret key for encryption and decryption, and both sides in the communication should get this key and keep its secrecy.

In asymmetric encryption system, the encryption key (public key) and decryption (secret key) are different.

Symmetric encryption algorithm:

- DES: Data Encryption Standard，fast, suitable for encrypting loads of data.
- 3DES（Triple DES）：Based on DES, use 3 different secret keys to encrypt 3 times for one block of data, high intensity.
- AES: Advanced Encryption Standard, the encryption algorithm standard of the next version, fast, high level of security.

Asymmetric encryption：

- RSA：Invented by RSA company, a public secret key algorithm supporting variable length key. The length of the file block that needs to be encrypted is also variable.
- DSA: Digital Signature Algorithm. A standard DSS (Digital Signature standard) .
- ECC: Elliptic Curves Cryptography.

Hash algorithm：

- MD5（Message Digest Algorithm 5）：A one-way hash algorithm invented by RSA data security company.
- SHA（Secure Hash Algorithm）：It generate a 160-bit number from the operation of data of any length.

[OpenSSL](http://www.openssl.org) is another famous cryptography algorithm library. It's a security protocol that offer security and data integrity for internet communication. Besides, it includes the main cryptography algorithms, common secret keys certificate packaging management function and SSL protocol. In addition, it offers many applications for testing and the use of other goals. Comparing Crypto++ and OpenSSL, we can see that the algorithms Crypto++ supports are more than OpenSSL.

## 3. Install Crypto++

There're two ways to install Crypto++:

- 1 Use `apt-get` to install directly
- 2 Download source code from the [official website](http://www.cryptopp.com/#download) or get the source code from [github](https://github.com/weidai11/cryptopp).

#### 3.1 Use the Source of Ubuntu to Install

```sh
sudo apt-get update
apt-cache pkgnames | grep -i crypto++
```


![image desc](https://labex.io/upload/K/U/B/BaWWP5OhdSmD.png)


```sh
sudo apt-get install libcrypto++-dev libcrypto++-doc libcrypto++-utils libcrypto++9 libcrypto++9-dbg
```


![image desc](https://labex.io/upload/F/B/I/z49hkHgLhAOL.png)


#### 3.2 Test

 After the installment, write a test program to check whether it's successfully installed:

```sh
cd /home/labex/
vim test1.cpp
```

Create file `test1.cpp` in `/home/labex`. Content as follows:

```cpp
#include <iostream>
using std::cout;
using std::endl;

#include "cryptopp/integer.h"
using CryptoPP::Integer;

int main( int, char** ) {

  Integer i;

  cout << "i: " << i << endl;
  cout << "Yo, man!" << endl;

  return 0;
}
```

After coding, exit vim and compile the program

```sh
g++ -o test1 test1.cpp -lcryptopp # The lcryptopp here is the cryto++ library. It may be -lcrypto++ in fedora.
./test1
```


![image desc](https://labex.io/upload/K/V/F/T8uyM2HFAmDY.png)


```checker
- name: check if test1.cpp exist
  script: |
    #!/bin/bash
    ls /home/labex/test1.cpp
  error: We found you didn't create file "test1.cpp" in "/home/labex/".
- name: check if main exist in test1.cpp
  script: |
    #!/bin/bash
    grep main /home/labex/test1.cpp
  error: We found you didn't define "main()" function in "test1.cpp".
- name: check if test1 exist
  script: |
    #!bin/bash
    ls /home/labex/test1
  error: We found you didn't compile to generate "test1" file in "/home/labex".
```

## 4. Write and implement MD5 digest algorithm

The full name of MD5 is Message-Digest Algorithm 5, it was invented by the computer science lab of MIT and RSA Data Security Inc and developed from MD2/MD3/MD4. The actual application of MD5 is generate fingerprint from a message to avoid tampering. So it's usually used in the encryption storage of password, digital signature and data integrity test.

In many operating system, the password of users are saved by MD5 value (or other similar algorithms). When the user logs in, the system calculate the input password into MD5 value, and compare with the MD5 value saved in the system to verify the legality of the user. 

It's quite simple to generate MD5 value by crypto++ library, you just need to understand this function:

Here's the prototype of the function we use:

```cpp
StringSource (const std::string &string,
              bool pumpAll,
              BufferedTransformation *attachment=NU
```

`stringsource` is a source of character array and character string.  [Source](http://www.cryptopp.com/wiki/Source) is the source of data.

Crypto++ offers common source below:  

- File
- Random Number
- Socket
- String
- Windows Pipe

Please refer to the [official handbook](http://www.cryptopp.com/wiki/StringSource)  for more details. 

Open the terminal and input:

```sh
cd /home/labex
vim md5.cpp
```

#### 4.1 Complete Code

```cpp
#define _CRYPTO_UTIL_H_
#define CRYPTOPP_ENABLE_NAMESPACE_WEAK 1
#include <iostream>
#include <string>
#include <cryptopp/md5.h>
#include <cryptopp/hex.h>
#include <cryptopp/files.h>
#include <cryptopp/default.h>
#include <cryptopp/filters.h>
#include <cryptopp/osrng.h>
using namespace CryptoPP;

int main()
{
  std::string digest, inData;
  std::cout << "please input a string" << std::endl;
  std::cin >> inData;
  Weak1::MD5 md5;
  StringSource(inData, true, new HashFilter(md5, new HexEncoder(new StringSink(digest))));

  std::cout<< digest <<std::endl;
}

```

#### 4.2 Compile and Generate:

```sh
g++ -o aes aes.cpp -lcryptopp
./md5
```


![image desc](https://labex.io/upload/A/T/L/FK2wvIrce418.png)


```checker
- name: checker if md5.cpp exist
  script: |
    #!/bin/bash
    ls /home/labex/md5.cpp
  error: We found you didn't create file "md5.cpp" in "/home/labex/".
```

## 5. Implement AES Encryption and Decryption

AES uses symmetric encryption, it's also called Rijndael encryption in cryptography and it's a block encryption standard used by the federal government of the United States. This standard is used to replace the former DES, already analyzed by many people and used all over the world

The design of AES has 3 secret key lengths: 128, 192, 256 bit. The 128 bit secret key of AES is 10^21 times more intensive than the 56 bit secret key of DES.

There are 5 encryption modes of AES:

- Electronics Code Book Mode (ECB mode) : 
  This mode divide the whole plaintext into some small parts in the same length, and encrypt each part.
- Cipher Block Chaining Mode（CBC mode）：This mode cut the plaintext into some parts, then after XOR every part and initial block or the ciphertext of the last part, encrypt with the secret key.
- Counter Mode（CTR mode）: It's a bit rare. In CTR mode, there's a auto-increment decrement operator. The operator use the input after secret key encryption and plaintext XOR to get the ciphertext, which means one-time pad.
- Cipher Feedback Mode（CFB mode）：ECB and CBC mode can only encrypt bulk data, but CFB can transfer bulk ciphertext into stream cipher..
- Output Feedback Mode（OFB mode）：OFB use bulk encryptor first to generate keystream, and then XOR the Keystream and plaintext stream to get ciphertext stream. The decryption use bulk encryptor first to generate keystream, and then XOR the keystream and ciphertext to get plaintext. Because of the symmetry of XOR, the operation of encryption and decryption are totally the same.

In this lab, we use CBC mode. While designing `class CCryptoUtil`, there're two modules: encrypt4aes encryption and decrypt4aes decryption.

#### 5.1 Create Encryption Module

Create file `aes.cpp` in `/home/labex/` and add the following code:

```cpp
static int encrypt4aes(const std::string &inData, const std::string &strKey,
        std::string &outData, std::string &errMsg)
{
    outData = "";
    errMsg = "";

    if (inData.empty() || strKey.empty()) // 
    Judge whether the encrypted character string and secret key is empty.
    {
        errMsg = "indata or key is empty!!";
        return -1;
    }

    unsigned int iKeyLen = strKey.length();

    if (iKeyLen != AES_KEY_LENGTH_16 && iKeyLen != AES_KEY_LENGTH_24  //Judge whether the length of the secret key meets the requirement
            && iKeyLen != AES_KEY_LENGTH_32)
    {
        errMsg = "aes key invalid!!";
        return -2;
    }

    byte iv[AES::BLOCKSIZE];
    int iResult = 0;

    try
    {
        CBC_Mode<AES>::Encryption e;  //CBC encryption
        e.SetKeyWithIV((byte*) strKey.c_str(), iKeyLen, iv);
        StringSource ss(inData, true, new StreamTransformationFilter(e, new StringSink(outData)));    //The key of encryption，outData is the encrypted data.
    } catch (const CryptoPP::Exception& e)
    {
        errMsg = "Encryptor throw exception!!";
        iResult = -3;
    }

    return iResult;
}
```
```checker
- name: check if aes.cpp exists
  script: |
    #!/bin/bash
    ls  /home/labex/aes.cpp
  error: We've found you didn't create file "aes.cpp" in "/home/labex/".
- name: check if encrypt4aes exist aes.cpp
  script: |
    #!/bin/bash
    grep -i 'static' /home/labex/aes.cpp | grep -i 'encrypt4aes'.
  error: We've found you didn't define "encrypt4aes()" function in "aes.cpp".
```

#### 5.2 Design the Decryption Module

Add the following code in /home/labex/aes.cpp:

```cpp
static int decrypt4aes(const std::string &inData, const std::string &strKey,
        std::string &outData, std::string &errMsg)
{
    outData = "";
    errMsg = "";

    if (inData.empty() || strKey.empty()) // Judge whether the encrypted character string and secret key is empty.
    {
        errMsg = "indata or key is empty!!";
        return -1;
    }

    unsigned int iKeyLen = strKey.length();

    if (iKeyLen != AES_KEY_LENGTH_16 && iKeyLen != AES_KEY_LENGTH_24  //Judge whether the length of the secret key meets the requirement
            && iKeyLen != AES_KEY_LENGTH_32)
    {
        errMsg = "aes key invalid!!";
        return -2;
    }

    byte iv[AES::BLOCKSIZE];
    int iResult = 0;

    try
    {
        CBC_Mode<AES>::Decryption d;    //CBC encryption
        d.SetKeyWithIV((byte*) strKey.c_str(), iKeyLen, iv);
        StringSource ss(inData, true,
                new StreamTransformationFilter(d, new StringSink(outData)));  //The decryption function. outData is the result of decryption.
    }
    catch (const CryptoPP::Exception& e)
    {
        errMsg = "Encryptor throw exception";
        iResult = -3;
    }

    return iResult;
}
```

```checker
- name: check if decrypt4aes exist aes.cpp
  script: |
    #!/bin/bash
    grep -i 'static' /home/labex/aes.cpp | grep -i 'decrypt4aes'
  error: We've found you didn't define "decrypt4aes()" function in "aes.cpp".
```

#### 5.3 Main Function

Add the following code in `/home/labex/aes.cpp`：

```cpp
int main(int argc, char **argv)
{
    std::string strCipher;     //The character string to be encrypted
    std::string strKey；       //The secret key to encrypt and decrypt
    std::cout << "Please enter a string" << std::endl;
    std::cin >> strCipher;
    std::cout << "please enter a key, you just can write 16,24 or 32 words as a key" << std::endl;
    std::cin << strKey;

    std::string strResult;
    std::string strErrMsg;
    int iResult = CCryptoUtil::encrypt4aes(strCipher, strKey, strResult, strErrMsg);
    std::cout << "the result is :" << strResult << std::endl;
    
    if(iResult)   
    {
        std::cout<<"CCryptoUtil::encrypt4aes failed,errMsg:"<<strErrMsg;
        return -1;
    }

    std::string strPlainText;
    iResult = CCryptoUtil::decrypt4aes(strResult,strKey,strPlainText,strErrMsg);
    if(iResult)
    {
        std::cout<<"CCryptoUtil::decrypt4aes failed,errMsg:"<<strErrMsg;
        return -2;
    }

    std::cout << "PlainText:"<<strPlainText << std::endl;
}
```

Here's the complete code for you to compile directly:

```sh
wget https://labexfile.oss-us-west-1-internal.aliyuncs.com/courses/87/aes.cpp
```

![image desc](https://labex.io/upload/S/L/P/4b0lZFoe2IBw.png)

```checker
- name: check if main exist aes.cpp
  script: |
    #!/bin/bash
    grep -i "main" /home/labex/aes.cpp
  error: We've found that you didn't define "main()" function in "aes.cpp".
```

## 6. Summary

In this lab, we've learned to install crypto++ library, and learned basic ways to use it. Besides, we got to know basic knowledge of MD5 and AES, and implemented the application of them. But while implementing AES encryption and decryption, we didn't print the encrypted string. Because it became gibberish while being input to the screen. What should we do? Please think about it.

