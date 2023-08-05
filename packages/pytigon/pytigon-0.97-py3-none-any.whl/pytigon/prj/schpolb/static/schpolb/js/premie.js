// Transcrypt'ed from Python, 2020-02-23 20:53:14
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__,  __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from '../../sch/org.transcrypt.__runtime__.js';
var __name__ = '__main__';
export var produkcja_premie_click = function (button) {
	var form = jQuery (button).closest ('form');
	jQuery ('#produkcja_div').find ('i').removeClass ('fa-caret-right');
	jQuery ('#produkcja_div').find ('i').removeClass ('fa-thumbs-down');
	jQuery ('#produkcja_div').find ('i').addClass ('fa-clock-o');
	jQuery ('#produkcja_div').find ('span').html ('');
	jQuery (button).attr ('data-style', 'zoom-out');
	jQuery (button).attr ('data-spinner-color', '#FF0000');
	window.WAIT_ICON = Ladda.create (button);
	window.WAIT_ICON.start ();
	var data_filter0 = function (data) {
		data.append ('proc_id', 0);
		return data;
	};
	var complete0 = function (data) {
		var on_end = function () {
			var data_filter1000 = function (data) {
				data.append ('proc_id', 1000);
				return data;
			};
			var complete1000 = function (data) {
				if (window.WAIT_ICON) {
					window.WAIT_ICON.stop ();
				}
				jQuery ('#produkcja_ul_1000').find ('i').removeClass ('fa-clock-o');
				jQuery ('#produkcja_ul_1000').find ('i').removeClass ('fa-thumbs-down');
				jQuery ('#produkcja_ul_1000').find ('i').addClass ('fa-check');
			};
			ajax_submit (form, complete1000, data_filter1000);
		};
		var gen_localisation = function (elements) {
			var element = elements.py_pop ();
			var id = int (jQuery (element).attr ('href'));
			var data_filter = function (data) {
				data.append ('proc_id', id);
				data.remove;
				return data;
			};
			var complete = function (data) {
				if (jQuery.trim (data) == 'OK') {
					jQuery (element).find ('i').removeClass ('fa-clock-o').addClass ('fa-check');
					jQuery (element).find ('span').html (data);
					if (elements.length > 0) {
						gen_localisation (elements);
					}
					else {
						on_end ();
					}
				}
				else {
					jQuery (element).find ('i').removeClass ('fa-clock-o').addClass ('fa-thumbs-down');
					jQuery (element).find ('span').html (data);
					if (elements.length > 0) {
						gen_localisation (elements);
					}
					else {
						on_end ();
					}
				}
			};
			ajax_submit (form, complete, data_filter);
		};
		if (jQuery.trim (data) == 'OK') {
			jQuery ('#produkcja_ul_0').find ('i').removeClass ('fa-clock-o').addClass ('fa-check');
			var ul = jQuery ('#produkcja_ul');
			var lokalizacje = jQuery.makeArray (ul.find ('li'));
			lokalizacje.reverse ();
			gen_localisation (lokalizacje);
		}
		else {
			jQuery ('#produkcja_div').find ('i').removeClass ('fa-clock-o');
			jQuery ('#produkcja_div').find ('i').removeClass ('fa-caret-right');
			jQuery ('#produkcja_div').find ('i').addClass ('fa-thumbs-down');
			if (window.WAIT_ICON) {
				window.WAIT_ICON.stop ();
			}
			jQuery ('#produkcja_ul_0').find ('span').html (jQuery.trim (data));
		}
	};
	ajax_submit (form, complete0, data_filter0);
	return false;
};
window.produkcja_premie_click = produkcja_premie_click;

//# sourceMappingURL=input.map