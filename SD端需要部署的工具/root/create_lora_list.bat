set "source_dir=%cd%"
set "target_dir=%cd%\models\Lora"
cd "%target_dir%"
del "%source_dir%\Lora_list.txt"
for %%f in (*.safetensors,.*ckpt) do (echo %%~nf >>"%source_dir%\Lora_list.txt")
pause